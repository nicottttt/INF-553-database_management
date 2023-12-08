from django.template import loader
from django.shortcuts import render
from django.core.paginator import Paginator
import psycopg2
import configparser
import os


def journal(request):

    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    config.read(config_file_path)
    host = "localhost"
    database = "pubmed"
    user = config.get('DATABASE', 'postgres_user_name')
    password = config.get('DATABASE', 'postgres_user_password')
    port = 5432

    con = psycopg2.connect(host=host,database=database,  user=user, password=password, port=port)
    cur = con.cursor()
    cur.execute("SELECT DISTINCT journal_title FROM pubmed_article ORDER BY journal_title ASC")
    journals = cur.fetchall()
    cleaned_journals = [(journal[0].replace('/', '%2F'),journal[0]) + journal[1:] for journal in journals] #Replace all the '/' to "%2F"


    # Pagination
    paginator = Paginator(cleaned_journals, 200)  # Show 200 journals per page.
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'journal.html', {'page_obj': page_obj})

def journal_detail(request, journal_name):

    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    config.read(config_file_path)
    host = "localhost"
    database = "pubmed"
    user = config.get('DATABASE', 'postgres_user_name')
    password = config.get('DATABASE', 'postgres_user_password')
    port = 5432

    con = psycopg2.connect(host=host,database=database,  user=user, password=password, port=port)
    cur = con.cursor()
    journal_name_new = journal_name.replace('%2F', '/') #Convert back to the original name wit '/'
    
    query = """ SELECT DISTINCT pa.author_name FROM pubmed_article AS pma JOIN article_author AS aa ON pma.article_id = aa.article_id JOIN pubmed_author AS pa ON aa.author_id = pa.author_id WHERE pma.journal_title = %s ORDER BY pa.author_name ASC; """ 
    cur.execute(query, (journal_name_new,))

    authors = cur.fetchall()
    cleaned_authors = [(author[0].replace('\'', '%27'),author[0]) + author[1:] for author in authors]
    
    return render(request, 'journal_detail.html', {'journal_name': journal_name_new, 'authors': cleaned_authors})

def author(request, author_name):
    
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    config.read(config_file_path)
    host = "localhost"
    database = "pubmed"
    user = config.get('DATABASE', 'postgres_user_name')
    password = config.get('DATABASE', 'postgres_user_password')
    port = 5432

    con = psycopg2.connect(host=host,database=database,  user=user, password=password, port=port)
    cur = con.cursor()
    author_name_new = author_name.replace('%27', '\'') 

    query = """
SELECT 
    pma.article_id,
    pma.title AS article_title,
    pma.year AS article_year,
    pma.pubmed_link,
    pma.journal_title,
    STRING_AGG(DISTINCT pa.author_name, ', ' ORDER BY pa.author_name) AS authors,
    STRING_AGG(DISTINCT gi.grant_val, ', ') AS grant_info,
    STRING_AGG(DISTINCT ac.coi_text, ', ') AS conflict_of_interest
FROM 
    pubmed_article pma
JOIN 
    article_author aa ON pma.article_id = aa.article_id
JOIN 
    pubmed_author pa ON aa.author_id = pa.author_id
LEFT JOIN 
    article_grant ag ON pma.article_id = ag.article_id
LEFT JOIN 
    grant_info gi ON ag.grant_id = gi.grant_id
LEFT JOIN 
    article_coi ac ON pma.article_id = ac.article_id
WHERE 
    EXISTS (
        SELECT 1 
        FROM article_author aa_inner
        JOIN pubmed_author pa_inner ON aa_inner.author_id = pa_inner.author_id
        WHERE aa_inner.article_id = pma.article_id AND pa_inner.author_name = %s
    )
GROUP BY 
    pma.title, pma.year, pma.pubmed_link, pma.journal_title, pma.article_id
ORDER BY 
    pma.year DESC, pma.journal_title, pma.article_id;
"""
    cur.execute(query, (author_name_new,))
    whole_list = cur.fetchall()
    
    

    return render(request, 'author.html', {'author_name': author_name, 'whole_list': whole_list})
