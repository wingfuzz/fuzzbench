import pandas as pd 
import pyecharts.options as opts
from pyecharts.charts import Line
import os 

def draw_line(datas, title, subtitle):
    line = Line(init_opts=opts.InitOpts(width="800px", height="400px", bg_color="white", page_title=f"开源FUZZ性能对比-{title}-{subtitle}"))
    line.add_xaxis(xaxis_data=list(range(len(datas))))
    line.add_yaxis(
        series_name=f"{title}-{subtitle}",
        y_axis=datas,
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
		

def main():
    df = pd.read_csv("/tmp/fuzzbench/coverage/coverage.txt", header=None, encoding="utf-8")
    projects = set(df[2])
    for p in projects:
        pd_project = df.loc[df[2] == p]
        pro_covs = pd_project[5].to_list()[:30]
        draw_line(pro_covs, p, "coverage")

    crashe_df = pd.read_csv("/tmp/fuzzbench/coverage/crashe.txt", header=None, encoding="utf-8")
    projects = set(crashe_df[2])
    for p in projects:
        pd_project = crashe_df.loc[crashe_df[2] == p]
        pro_crashes = pd_project[3].to_list()[:30]
        draw_line(pro_crashes, p, "crashe")


if __name__ == "__main__":
    main()

