import os
import json
import yaml
from anthropic import Anthropic

# read key from .env
with open(".env", "r") as f:
    api_key = f.read()

# Initialize the Anthropic client
client = Anthropic(api_key=api_key)


# re-write the categories yaml
def re_write_cat_yamls(paper, categories_yaml):
    classification_prompt = f"""
    Your task is to categorize AI Alignment research papers.
    I will provide you with title, abstract and url of an alignment research paper.
    I will also provide you with the current categories (categories_yaml).
    Your task is to re-write the categories_yaml with the new paper added to the appropriate category.
    You can create new main categories or sub-categories as needed.
    One paper can be in multiple categories.
    Aim for conciseness of main and sub-categories.
    DO NOT WRITE ANYTHING OTHER THAN THE CONTENTS of categories_yaml.
    Here is the content of the paper:
    - title: {paper["title"]}
    - abstract: {paper["abstract"]}

    The current categories are:
    {categories_yaml}
    """

    print(classification_prompt)

    message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            messages=[
                {
                    "role": "user", 
                    "content": classification_prompt}
            ]
        )

    out = message.content[0].text
    return out


if __name__ == '__main__':
    papers_yaml = "./arxiv_papers_for_llm.yaml"

    # read the papers yaml
    with open(papers_yaml, "r", encoding="utf-8") as f:
        papers = yaml.safe_load(f)

    # starting template for the clustering
    categories_yaml = "./llm_cluster_start.yaml"

    # iterate over 20 papers at the same time instead of single paper
    

    for paper in papers:
        # read the categories yaml as it is
        with open(categories_yaml, "r", encoding="utf-8") as f:
            categories = f.read()

        # re-write the yaml file
        out = re_write_cat_yamls(paper, categories)
        
        # ensure its correct
        categories = yaml.safe_load(out)
        
        # overwrite the categories yaml
        with open("llm_cluster.yaml", "w") as f:
            f.write(out)

        categories_yaml = "llm_cluster.yaml"



