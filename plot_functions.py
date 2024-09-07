from matplotlib import pyplot as plt


def prepare_plot(freq_dict: dict, n_rows: int, n_cols: int,
                 p_title: str, f_path=None, save_figure=False):
    # prepare data for plotting:
    data_frames = list(freq_dict.values())
    doc_names = list(freq_dict.keys())
    sorted_frames = []
    for df in data_frames:
        sorted_df = df.sort_values(by='frequency', ascending=False).head(15).sort_values(by='frequency')
        sorted_frames.append(sorted_df)
    # plot data
    nrows = n_rows
    ncols = n_cols
    fig, ax = plt.subplots(nrows, ncols, figsize=(10, 8))
    count = 0
    for x in range(nrows):
        for y in range(ncols):
            try:
                df = sorted_frames[count]
                title = doc_names[count]
            except IndexError:
                break
            ax[x, y].barh(df.word, df.frequency)
            ax[x, y].set_title(title)
            count += 1
    plt.suptitle(p_title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to prevent overlap of the columns
    plt.subplots_adjust(top=0.90, hspace=0.3)  # reduce the space between columns and suptitle
    if save_figure:
        plt.savefig(f_path)
    plt.show()
