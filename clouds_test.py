# *-* coding: utf-8 *-*
''' 对AWS, Aliyun, Oracle, Baidu, Huawei, Tencent, Linode, Ucloud, Vultr全球的数据中心进行ping测试
'''
import pandas as pd
import ping3
import argparse
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from concurrent.futures import ThreadPoolExecutor, as_completed

console = Console()

def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        console.print(f'读取({file_path})文件失败: {e}', style='red')
        return None


def filter_cloud_providers(data, locations, clouds):
    filtered_data = data

    if clouds:
        filtered_data = filtered_data[filtered_data['cloud'].isin(clouds)]
        if filtered_data.empty:
            console.print(f'没有找到厂商名称包含以下关键字的节点: {clouds}', style='red')
            available_clouds = data['cloud'].unique()
            console.print(f'有效的厂商有: {", ".join(available_clouds)}', style='green')

    if locations:
        filtered_data = filtered_data[filtered_data['location'].str.contains('|'.join(locations))]
        if filtered_data.empty:
            console.print(f'没有找到位置名称包含以下关键字的节点: {locations}', style='red')

    return filtered_data


def ping_host(host):
    ping3.EXCEPTIONS = True
    try:
        result = ping3.ping(host, unit='ms')
        return result
    except Exception as e:
        console.print(f'Ping {host} 失败: {e}', style='red')
        return -1


def test_ping_task(node):
    avg_time = ping_host(node['endpoint'])
    color = color_for_time(avg_time)
    console.print(f'[{color}]{node["cloud"]}\t{node["location"]}: {avg_time:.2f}ms[/]')
    return node['cloud'], node['location'], avg_time, color


def color_for_time(avg_time):
    if avg_time == -1:
        return 'red'
    elif avg_time < 100:
        return 'green'
    elif avg_time < 200:
        return 'yellow'
    else:
        return 'red'


def print_results_table(df):
    table = Table(show_header=True, header_style='bold magenta')
    table.add_column('厂商')
    table.add_column('位置')
    table.add_column('延迟(ms)', justify='right')
    for _, row in df.iterrows():
        time_str = 'N/A' if row['ping'] == -1 else f'{row["ping"]:.2f}'
        table.add_row(row['cloud'], row['location'], time_str, style=row['color'])
    console.print(table)


def main(file_path, clouds, locations, top_n):
    data = load_data(file_path)
    if data is not None:
        data = filter_cloud_providers(data, locations, clouds)

    if data.empty:
        return

    results = []
    with Progress(console=console) as progress:
        task = progress.add_task('Testing...', total=len(data))
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(test_ping_task, node): node for _, node in data.iterrows()}
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                progress.update(task, advance=1)

    results_df = pd.DataFrame(results, columns=['cloud', 'location', 'ping', 'color'])
    console.print('[bold]所有节点测试结果:[/bold]')
    print_results_table(results_df.sort_values(['cloud', 'ping']))

    results_df.drop(results_df[results_df['ping'] == -1].index, inplace=True)
    location_df = results_df['location']
    domestic_filter = location_df.str.contains('China') & ~location_df.str.contains('Hong Kong') & ~location_df.str.contains('Taipei')
    for label, group_df in [('国内', results_df[domestic_filter]), ('海外', results_df[~domestic_filter])]:
        top_results = group_df.nsmallest(min(top_n, len(group_df)), 'ping')
        if top_results.empty:
            continue
        console.print(f'\n[bold]{label}速度前{top_n}名:[/bold]')
        print_results_table(top_results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='测试云厂商节点的ping速度，支持并发执行。')
    parser.add_argument('-f', '--file', type=str, default='cloud_servers.csv', help='指定CSV文件的路径，默认为cloud_servers.csv。')
    parser.add_argument('-c', '--cloud', nargs='+', help='指定要测试的云厂商，可以是多个。')
    parser.add_argument('-l', '--location', nargs='+', help='指定要测试的位置，可以是多个。')
    parser.add_argument('-t', '--top', type=int, default=5, help='指定要分区展示的前几名速度，默认为5。')
    args = parser.parse_args()
    main(args.file, args.cloud, args.location, args.top)
