from wikiflix.db import db_inst

session = db_inst.session

Model = db_inst.Model
metadata = Model.metadata

relationship = db_inst.relationship

Table = db_inst.Table
Column = db_inst.Column

ForeignKey = db_inst.ForeignKey

select = db_inst.select

Integer = db_inst.Integer
String = db_inst.String
Float = db_inst.Float
Blob = db_inst.BLOB

