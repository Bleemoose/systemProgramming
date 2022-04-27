from random import random

import Monitoring
import concurrent.futures
import requests
import urllib.request
import time
import bs4
import concurrent.futures
import _thread
import multiprocessing
import psutil
import threading

wikipedia_urls_path = "./wikipedia_urls.txt"
positive_words_path = "./positive_words.txt"
negative_words_path = "./negative_words.txt"
file = open(wikipedia_urls_path, "r")
file_content = file.read()
articles_urls = file_content.split('\n')

def article_scraper (url):
  response = requests.get(url)
  if response is not None:
    html = bs4.BeautifulSoup(response.text, 'html.parser')
    title = html.select("#firstHeading")[0].text
    paragraphs = html.select("p")
    textual_data = " " .join([ para.text for para in paragraphs[0:5]])
  return textual_data.split(" ")

def pos_neg_words( path_pos, path_neg):
  file_pos = open(path_pos, "r")
  file_pos_content = file_pos.read()
  lpositive_words = file_pos_content.split('\n')
  file_neg = open(path_neg, "r")
  file_neg_content = file_neg.read()
  lnegative_words = file_neg_content.split('\n')
  return lpositive_words, lnegative_words

def article_sentiment_analysis(num_article):
  lpos_words, lneg_words = pos_neg_words(positive_words_path,negative_words_path)
  article_words = article_scraper(articles_urls[num_article])
  spos_words , sneg_words, sarticle_words = set(lpos_words), set(lneg_words), set(article_words)
  num_pos_words = len(spos_words.intersection(sarticle_words))
  num_neg_words = len(sneg_words.intersection(sarticle_words))
  #print(num_pos_words,num_neg_words, end=" ")
  if num_pos_words == num_neg_words or num_pos_words +1 == num_neg_words or num_pos_words == num_neg_words +1: return articles_urls[num_article].split("/")[-1], "neutral"
  return (articles_urls[num_article].split("/")[-1], "positive") if num_pos_words > num_neg_words else (articles_urls[num_article].split("/")[-1], "negative")

def dumb_run():
  mem = psutil.virtual_memory()


  print("Nuber of CPUs: ", psutil.cpu_count(), " Total physical memory", str(int(mem.total / 1024 ** 2)), "MB")
  start_time = time.time()
  for i in range(100):
    print("%s : %s" % article_sentiment_analysis(i))
  # monitor_CPU_Ram()
  print("Execution time: ", str((time.time() - start_time)))



def myThread(i):
  print("%s : %s" % article_sentiment_analysis(i))

def threads(N):
  mem = psutil.virtual_memory()

  print("Nuber of CPUs: ", psutil.cpu_count(), " Total physical memory", str(int(mem.total / 1024 ** 2)), "MB")
  start_time = time.time()
  threads = []
  with concurrent.futures.ThreadPoolExecutor(N) as executor:
    executor.map(myThread, range(100))
  print("Execution time: ", str((time.time() - start_time)))



def multiproccessRun(N):
  mem = psutil.virtual_memory()
  print("Nuber of CPUs: ", psutil.cpu_count(), " Total physical memory", str(int(mem.total / 1024 ** 2)), "MB")
  start_time = time.time()
  with concurrent.futures.ProcessPoolExecutor(N) as exe:
    exe.map(myThread, range(100))
  print("Execution time: ", str((time.time() - start_time)))

if __name__ == "__main__":

    mon_obj = Monitoring.VizualizeMonitoring([], [])
    t1 = threading.Thread(target=mon_obj.monitor_cpu, args=(50,))
    t2 = threading.Thread(target=mon_obj.monitor_ram, args=(50,))
    t1.start()
    t2.start()
    threads(3)
    mon_obj()