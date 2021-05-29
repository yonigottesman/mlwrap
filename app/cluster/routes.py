from io import StringIO, BytesIO

from flask import (
    render_template, redirect, url_for, send_file,
)
from sklearn.decomposition import PCA

from app.cluster import bp
from app.cluster.forms import KmeansForm
from sklearn.cluster import KMeans
import pandas as pd
import plotly.express as px


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def index():
    form = KmeansForm(n_clusters=8,
                      init='k-means++',
                      n_init=10,
                      max_iter=300,
                      tol=0.0001,
                      algorithm='auto'
                      )
    if form.validate_on_submit():
        estimator = KMeans(**{x: y for x, y in form.data.items()
                              if x in ['n_clusters', 'init', 'n_init', 'max_iter', 'tol', 'algorithm']})
        file = form.csv.data
        data = pd.read_csv(file, header=None)
        estimator.fit(data)

        if form.download.data is True:
            buffer = BytesIO()

            data['label'] = estimator.labels_
            data.to_csv(buffer, header=False, index=False)
            buffer.seek(0)
            return send_file(
                buffer,
                as_attachment=True,
                attachment_filename='test.csv',
                mimetype='text/csv')
        elif form.visualize.data is True:
            pca = PCA(n_components=3).fit(data)
            data_3d = pca.transform(data)
            df = pd.DataFrame(data_3d)
            df['label'] = estimator.labels_
            df['label'] = df['label'].apply(str)
            fig = px.scatter_3d(df, x=0, y=1, z=2,
                                color='label')

            buffer = StringIO()
            fig.write_html(buffer)
            buffer.seek(0)
            return render_template("cluster/index.html",
                                   form=form, chart=buffer.read())

    return render_template("cluster/index.html",
                           form=form, )
