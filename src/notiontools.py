from notion.client import NotionClient
from notion.block import CollectionViewBlock
from notion.block import *

client = NotionClient(
    token_v2="75dd8c89f5f08505507d5502edda67fd2d83d0a2dff0654619d813850e65bc692b1d3d94ef61f1a9c86412259ee14b37ec27c827e9fe1e06548ef238c552d9fd01d62fd76be5df6f2b40c5e0cac9")
cv = client.get_collection_view(
    'https://www.notion.so/f254c4788c7d45519ac009c05045de34?v=763496891285406fa7929944f0ee9fb5')
# coll = client.get_collection(cv.collection.id)
# table = client.get_record_data(coll._table, cv.collection.id)
# table.update({'name':'Tags','type':'text'})
# coll.set("schema.property.tags.type",'')
# coll.refresh()
# table['schema']['(N8e']['type'] = 'text'
# print(table)
# table.update()

def deleteRows():
    for row in cv.collection.get_rows():
        row.remove()


def addRows(data):
    cv.build_query()
    for company, position, link, score, tags in data:
        row = cv.collection.add_row()
        row.company = company
        row.position = position
        row.link = link
        row.score = score
        row.applied = False
        row.tags = tags.split(',')
# table['schema']['(N8e']['type'] = 'multi_select'
#
#
# data = [('Vintory', 'Data Analyst',
#          'http://www.linkedin.com/jobs/view/1925410525/?eBP=JYMBII_JOBS_HOME_ORGANIC&recommendedFlavor=ACTIVELY_HIRING_COMPANY&refId=ac7425a5-be23-425a-a023-a4f9bc26a294&trk=flagship3_jobs_discovery_jymbii',
#          20, 'Python'),
#         ('Toyota North America', 'Data Science Analyst',
#          'http://www.linkedin.com/jobs/view/1901513255/?eBP=JYMBII_JOBS_HOME_ORGANIC&recommendedFlavor=SCHOOL_RECRUIT&refId=ac7425a5-be23-425a-a023-a4f9bc26a294&trk=flagship3_jobs_discovery_jymbii',
#          160, "Python,Tableau,SQL"),
#         ('Precision Distribution Consulting', 'Project Analyst',
#          'http://www.linkedin.com/jobs/view/1924818800/?eBP=JYMBII_JOBS_HOME_ORGANIC&recommendedFlavor=SCHOOL_RECRUIT&refId=ac7425a5-be23-425a-a023-a4f9bc26a294&trk=flagship3_jobs_discovery_jymbii',
#          -210, "5-workex,SQL")]
#
# deleteRows()
# addRows(data)