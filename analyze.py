import pandas as pd 
import pyecharts.options as opts
from pyecharts.charts import Line
import os 
from config import SHARED_DIR

half_period = 360
point = 30

def weighted(values):
    """ 计算权值
    
    Args:
        values (_type_): _description_
    """
    weights = []
    for i in range(len(values)):
        w = 0.5 ** (i / 360) 
        weights.append(w)
    return weights


def weighted_average(values):
    """
    计算加权平均值

    :param values: 数值列表
    :param weights: 权重列表，与数值列表一一对应
    :return: 加权平均值
    """
    weights = weighted(values)
    return sum(values[i] * weights[i] for i in range(len(values))) / sum(weights)


def time_averaging(datas):
    d = {}
    for k in datas.keys():
        d[k] = weighted_average(datas[k])
    return d


def global_max(datas):
    d = {}
    for k in datas.keys():
        d[k] = max(datas[k])
    return d


def draw_line(datas, title, subtitle):
    print(datas)
    line = Line(init_opts=opts.InitOpts(width="800px", height="400px", bg_color="white", page_title=f"开源FUZZ性能对比-{title}-{subtitle}"))
    line.add_xaxis(xaxis_data=list(range(point)))

    for k in datas.keys():
        line.add_yaxis(
            series_name=k,
            y_axis=datas[k],
            is_smooth=True
		)
    line.set_global_opts(
            title_opts=opts.TitleOpts(title=None, subtitle=None, pos_left="15%"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
    line.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    save_path = os.path.join("/mnt/d/work/2023", f"{title}-{subtitle}.html")
    line.render(save_path)
    print(f"{save_path} written.")


def read_coverage(cov_path):
    df = pd.read_csv(cov_path, header=None, encoding="utf-8")
    new_df = pd.DataFrame({"fuzzer": df[1], "coverage": df[5] }, columns=["fuzzer", "coverage"])
    new_dict = dict()
    for k in list(set(new_df["fuzzer"])):
        data = new_df.loc[new_df["fuzzer"] == k]
        new_dict[k] = data["coverage"].to_list()[:point]

    return new_dict


def read_crashe(crashe_path):
    df = pd.read_csv(crashe_path, header=None, encoding="utf-8")
    new_df = pd.DataFrame({"fuzzer": df[1], "crashes": df[3]}, columns=["fuzzer", "crashes"])
    print(new_df.shape)
    new_df = new_df[:30]
    print(new_df.shape)
    new_dict = dict()
    for k in list(set(new_df["fuzzer"])):
        data = new_df.loc[new_df["fuzzer"] == k]
        new_dict[k] = data["crashes"].to_list()[:point]

    return new_dict


def total_scores(total_scores_datas):
    global_cov_max_fuzzer = max(total_scores_datas, key=lambda k: total_scores_datas[k])
    max_value = total_scores_datas[global_cov_max_fuzzer]
    new_dict = {}
    for k, v in total_scores_datas.items():
        new_dict[k] = v / max_value * 100
    return new_dict


def report(project, cov_values, crashe_values):
    file = open("report.txt", mode="a+", encoding="utf-8")
    p_name = f"Project: {project}\n"
    file.write(p_name)
    total_score_dict = {}
    d = global_max(cov_values)
    for key, value in d.items():
        file.write(f"\tfuzzer: {key}, global coverage: {value}\n")
        try:
            total_score_dict[key] += value 
        except KeyError:
            total_score_dict[key] = value 

    d = global_max(crashe_values)
    for key, value in d.items():
        file.write(f"\tfuzzer: {key}, global detection rate: {value}\n")
        try:
            total_score_dict[key] += value 
        except KeyError:
            total_score_dict[key] = value 
    d = time_averaging(cov_values)
    for key, value in d.items():
        file.write(f"\tfuzzer: {key}, time average coverage: {value}\n")
        try:
            total_score_dict[key] += value 
        except KeyError:
            total_score_dict[key] = value 
    d = time_averaging(crashe_values)
    for key, value in d.items():
        file.write(f"\tfuzzer: {key}, time average detection rate: {value}\n")
        try:
            total_score_dict[key] += value 
        except KeyError:
            total_score_dict[key] = value 
    stability = 1
    file.write(f"\tnormal rate of stability: {stability}\n")

    scores = total_scores(total_score_dict)
    for k, v in scores.items():
        file.write(f"\tfuzzer: {k}, score: {v}\n")

    file.write("--------------------------------------------\n\n")

    return scores


def main():
    coverage_dir =  os.path.join(SHARED_DIR, "coverage")
    project_number = 0
    score_dict = {}
    for i in os.listdir(coverage_dir):
        project_number += 1
        project_dir = os.path.join(coverage_dir, i)
        coverage_file = os.path.join(project_dir, "coverage.txt")
        cov_values = read_coverage(coverage_file)
        draw_line(cov_values, i, "Coverage")
        crashe_file = os.path.join(project_dir, "crashe.txt")
        crashe_values = read_crashe(crashe_file)
        draw_line(crashe_values, i, "Crashes")
        score = report(i, cov_values, crashe_values)
        for key, value in score.items():
            try:
                score_dict[key] += value 
            except KeyError:
                score_dict[key] = value 

    file = open("report.txt", mode="a+", encoding="utf-8")
    sorted_values = sorted(score_dict.items(), key=lambda x: x[1])
    for k, v in sorted_values:
        score = v / project_number
        file.write(f"\tfuzzer: {k}, score: {score}\n")
    file.write("--------------------------------------------\n\n")

if __name__ == "__main__":
    main()

