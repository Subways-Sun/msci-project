"""Module for processing literature data."""
# pylint: disable=locally-disabled, line-too-long, invalid-name
import json

def read_json(json_file_path):
    """Function to read a JSON file"""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def write_json(json_file_path, data):
    """Function to write to a JSON file"""
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def combine_json_files(output_file_path, *json_file_paths):
    """Function to combine multiple JSON files into one"""
    combined_data = []

    for file_path in json_file_paths:
        data = read_json(file_path)
        combined_data.extend(data)

    write_json(output_file_path, combined_data)

def remove_duplicates(input_dict):
    """Function to remove duplicates from a dictionary list"""
    unique_entries = []
    seen_ids = set()

    for entry in input_dict:
        entry_id = entry.get('paperId')
        if entry_id not in seen_ids:
            unique_entries.append(entry)
            seen_ids.add(entry_id)

    return unique_entries

def keep_journal(input_dict):
    """Function to only retain journal articles in a dictionary list"""
    journal = []
    for entry in input_dict:
        if entry.get('publicationTypes') == ['JournalArticle']:
            journal.append(entry)

    return journal

def remove_no_abstract(input_dict):
    """Function to remove papers with no abstract from a dictionary list"""
    with_abstract = []
    for entry in input_dict:
        if entry.get('abstract'):
            with_abstract.append(entry)

    return with_abstract

def keep_select_publishers(input_dict, publishers: list):
    """Function to only retain papers from select publishers in a dictionary list"""
    selected_list = []
    for entry in input_dict:
        if entry.get('externalIds').get('DOI'):
            if entry.get('externalIds').get('DOI').split('/')[0] in publishers:
                selected_list.append(entry)

    return selected_list

def keep_relevant(input_dict, label: str):
    """Function to only retain relevant papers in a labelled dictionary list"""
    relevant_list = []
    for entry in input_dict:
        if entry.get(label) == 1:
            relevant_list.append(entry)

    return relevant_list
