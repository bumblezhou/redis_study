import redis
import json
from redis.commands.json.path import Path
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

client = redis.Redis(host='localhost', port=6379)

doc_1 = {
    'ContractName': 'Elementary school rebuilding',
    'ContractContent': 'The ceremony marks the beginning of construction at the $125 million project, which includes new construction of approximately 81,000 square feet and extensive renovations of 68,094 square feet to the existing building. The project also includes new furnishings and playground improvements. When complete, Bechtel Elementary will feature student-centered design elements including neighborhood instructional spaces and furnishings that support collaboration and community.During construction, Bechtel Elementary will continue to operate out of Kadena Elementary (Universal Prekindergarten, Kindergarten, and Preschool Services for Children with Disabilities) and Ryukyu Middle (grades 1-5). DoDEA plans, directs, coordinates, and manages Pre-Kindergarten through 12th grade education programs for school-aged children of Department of Defense personnel who would otherwise not have access to a high-quality public education. DoDEA schools are located in Europe, the Pacific, Western Asia, the Middle East, Cuba, the United States, Guam, and Puerto Rico. DoDEA also provides support and resources to Local Educational Activities throughout the U.S. that serve children of military families.',
    'AssociatedEmail': 'taro@example.com',
    'PublishDate': '2010-01-24',
    'ProjectName': 'Elementary school rebuilding',
    'AssociatedUnits': 'X distrit gov, A building company'
}

doc_2 = {
    'ContractName': 'Swimming pool repairing',
    'ContractContent': 'An outdoor swimming pool will be exposed to the elements and so they require plenty of care to keep them in good condition. The ground around your pool has the potential to shrink and expand, which can exacerbate any issues you may face over time. Whether you’ve had your pool for a long time or you’ve moved into a property that already had one, there are some common signs that it may be time to update it. The first is cracks in the structure of the pool. While this may be alarming to see, there are varying levels of damage that could be at play, and the placement and size of the damage will determine the scale of the issue. Surface level cracks in the concrete are known as craze cracks and while they may lead to other problems if they’re left to develop, they’re not necessarily a reason to immediately refurbish. But structural cracks are a bigger problem and can be costly to fix.',
    'AssociatedEmail': 'mia@example.com',
    'PublishDate': '2010-01-24',
    'ProjectName': 'Swimming pool repairing',
    'AssociatedUnits': 'C distrit Swimming pool, B building company'
}

doc_3 = {
    'ContractName': 'Library Renovation',
    'ContractContent': 'The purpose of library renovation can vary depending on the specific goals and needs of the library and its patrons. However, in general, library renovation is intended to improve the functionality, accessibility, and aesthetic appeal of the library in order to better serve the community and meet the changing needs of library users. Some specific goals of library renovation may include: 1. Updating and modernizing the library’s technology and equipment, such as computers, printers, and audiovisual systems. 2. Improving the library’s layout and space utilization to create a more efficient and comfortable environment for users, such as adding collaborative workspaces or quiet study areas. 3. Enhancing the library’s accessibility for people with disabilities, such as by installing ramps, elevators, or assistive technology. 4. Adding new amenities and services to the library, such as cafes, maker spaces, or specialized collections. 5. Upgrading the library’s infrastructure and systems, such as HVAC or lighting, to improve energy efficiency and sustainability. 6. Refreshing the library’s decor and furnishings to create a more inviting and attractive space for users.',
    'AssociatedEmail': 'jason@example.com',
    'PublishDate': '2010-01-24',
    'ProjectName': 'Library Renovation',
    'AssociatedUnits': 'X City Library, C building company'
}

client.json().set("doc:1", Path.root_path(), doc_1)
client.json().set("doc:2", Path.root_path(), doc_2)
client.json().set("doc:3", Path.root_path(), doc_3)

print(client.json().get("doc:1"))

schema = (
    TextField("$.ContractName", as_name="name"),
    TagField("$.AssociatedUnits", as_name="units"),
    TextField("$.ProjectName", as_name="project"),
    TextField("$.AssociatedEmail", as_name="email"), 
    TextField("$.PublishDate", as_name="date"),
    TextField("$.ContractContent", as_name="content")
)
client.ft().dropindex(delete_documents=False)
client.ft().create_index(schema, definition=IndexDefinition(prefix=["doc:"], index_type=IndexType.JSON))

res = client.ft().search("goals")
print(res.docs)
print(json.loads(res.docs[0].json))