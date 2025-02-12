"""Script to retrive relevant paper"""
# pylint: disable=locally-disabled, line-too-long, invalid-name
import os
from datetime import datetime
from sib.literature import semantic as ss
# from sib.literature import scopus as sc
from sib.literature import lit_processing as lp

# Define search parameters
query_list = ["sodium+ion+battery+anode",
          "sodium+ion+battery+cathode",
          "sodium+ion+battery+electrode",
          "sib+cathode",
          "sib+anode",
          "sib+electrode"]

fields = "externalIds,title,publicationTypes,publicationDate"
count = 3000 # Number of papers to retrieve for each keyword
publication_types = "JournalArticle" # Only retrieve journal articles
year = "2016-" # Only retrieve papers published after 2016

result = list([])
url_list = list([])

# Search for relevant papers
for query in query_list:
    result_temp = ss.search_bulk(query, count, fields = fields, publicationTypes = publication_types, year = year)
    data = result_temp[0]
    url = result_temp[1]
    print(f"Number of papers retrieved for '{query.replace('+', ' ')}': {len(data)}")
    result.extend(data)
    url_list.append(url)
print(f"\nFinished initial search, number of papers retrieved: {len(result)}")

# Remove duplicates
result = lp.remove_duplicates(result)
print(f"\nNumber of papers after removing duplicates: {len(result)}")

# Only keep papers from select publishers
publishers = ["10.1039", # RSC
              "10.1016", # Elsevier
              "10.1021", # ACS
              "10.1002", # Wiley
              "10.1007", # Springer
              "10.1080", # Taylor & Francis
              "10.1038"] # Nature
result = lp.keep_select_publishers(result, publishers)
print(f"\nNumber of papers from select publishers: {len(result)}")

# Retrieve abstract from Scopus
# for paper in result:
#     doi = paper.get("externalIds").get("DOI")
#     abstract = sc.search_paper_details(doi).get("abstract")
#     paper["abstract"] = abstract

# Remove papers with no abstract
# result = lp.remove_no_abstract(result)
# print(f"\nNumber of papers after removing papers with no abstract: {len(result)}")

# Save the search parameters to a json file
current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
params = {"searchKeywords": query_list, "fields": fields, "count": count, "publicationTypes": publication_types, "year": year, "result_len": len(result), "urls": url_list}
params_path = os.path.join(os.getcwd(), "data", f"search_{current_time}_params.json")
lp.write_json(params_path, params)

# Print the number of papers retrieved
print(f"\nNumber of papers retrieved: {len(result)}")

# Save the result to a json file
result_path = os.path.join(os.getcwd(), "data", f"search_{current_time}.json")
lp.write_json(result_path, result)
