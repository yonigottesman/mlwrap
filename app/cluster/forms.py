from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (IntegerField, SelectField, FloatField,
                     SubmitField)
from wtforms.validators import DataRequired


class KmeansForm(FlaskForm):
    n_clusters = IntegerField(label='n_clusters', validators=[DataRequired()])
    init = SelectField('init', choices=['k-means++', 'random'], validators=[DataRequired()])
    n_init = IntegerField(label='n_init', validators=[DataRequired()])
    max_iter = IntegerField(label='max_iter', validators=[DataRequired()])
    tol = FloatField('tol', validators=[DataRequired()])
    algorithm = SelectField('algorithm', choices=['auto', 'full', 'elkan'], validators=[DataRequired()])
    csv = FileField('data', validators=[DataRequired()])
    download = SubmitField('download')
    visualize = SubmitField('visualize', render_kw={'class': 'btn-danger'})