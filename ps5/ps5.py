# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Chase Zelechowski
# Collaborators: n/a
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re
import copy


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
        #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


# ======================
# Data structure design
# ======================

# Problem 1

class NewsStory:
    def __init__(self, guid: str, title: str, description: str, link: str, pubdate: datetime):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


# ======================
# Triggers
# ======================


class Trigger:
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2

class PhraseTrigger(Trigger):

    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def evaluate(self, story):
        pass

    def is_phrase_in(self, text: str):
        # Clean input text and convert into list of words, convert phrase into list as well
        text, text_as_list = re.findall('[^!"#$%&()*+,-./:;<=>?@^_`{|}~]+', text.lower()), []
        for i in range(0, len(text), 1):
            split = text[i].split()
            for j in range(0, len(split), 1):
                text_as_list.append(split[j])
        phrase_as_list = self.phrase.split()

        # Check that entire phrase is in text
        for i in range(0, len(text_as_list), 1):
            if phrase_as_list[0] in text_as_list[i]:
                for j in range(1, len(phrase_as_list), 1):
                    if i + j < len(text_as_list):
                        if phrase_as_list[j] != text_as_list[i+j]:
                            return False
                    else:
                        return False
                return True
        return False


# Problem 3

class TitleTrigger(PhraseTrigger):
    def evaluate(self, story: NewsStory):
        return self.is_phrase_in(story.get_title())


# Problem 4

class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story: NewsStory):
        return self.is_phrase_in(story.get_description())


# TIME TRIGGERS

# Problem 5

class TimeTrigger(Trigger):
    def __init__(self, pubdate: str):
        try:
            self.pubdate = datetime.strptime(pubdate, '%d %b %Y %H:%M:%S %Z')
        except ValueError:
            self.pubdate = datetime.strptime(pubdate, '%d %b %Y %H:%M:%S')
            self.pubdate = self.pubdate.replace(tzinfo=pytz.timezone("EST"))

    def evaluate(self, story):
        pass


# Problem 6

class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        if story.pubdate.tzinfo is None:
            story.pubdate = story.pubdate.replace(tzinfo=pytz.timezone('EST'))
        return self.pubdate > story.pubdate


class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        if story.pubdate.tzinfo is None:
            story.pubdate = story.pubdate.replace(tzinfo=pytz.timezone('EST'))
        return self.pubdate < story.pubdate


# COMPOSITE TRIGGERS

# Problem 7

class NotTrigger(Trigger):
    def __init__(self, trigger: Trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)


# Problem 8

class AndTrigger(Trigger):
    def __init__(self, trigger1: Trigger, trigger2: Trigger):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)


# Problem 9

class OrTrigger(Trigger):
    def __init__(self, trigger1: Trigger, trigger2: Trigger):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


# ======================
# Filtering
# ======================

# Problem 10

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filtered_stories = []
    for i in range(0, len(stories), 1):
        for j in range(0, len(triggerlist), 1):
            current = triggerlist[j]
            if current.evaluate(stories[i]) is True:
                filtered_stories.append(stories[i])
    return filtered_stories


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    trigger_file = open(filename, 'r')
    lines = []
    created_triggers = {}
    added_triggers = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # Parse each line
    for i in range(0, len(lines), 1):
        line_as_list = lines[i].split(',')

        # Create triggers
        if line_as_list[0] != 'ADD':
            # Composite triggers
            if line_as_list[1] == "AND" or line_as_list[1] == "OR":
                created_triggers[line_as_list[0]] = get_composite_trig_type(line_as_list[1], line_as_list[2], line_as_list[3])
            # Non-composite triggers
            else:
                created_triggers[line_as_list[0]] = get_trig_type(line_as_list[1], line_as_list[2])

        # Add triggers to list
        else:
            for k in range(1, len(line_as_list), 1):
                added_triggers.append(created_triggers[line_as_list[k]])
    return added_triggers


def get_trig_type(trigtype: str, trigger_param) -> Trigger:
    dictionary = {
        'TITLE': TitleTrigger,
        'DESCRIPTION': DescriptionTrigger,
        'BEFORE': BeforeTrigger,
        'AFTER': AfterTrigger,
        'NOT': NotTrigger
    }
    return dictionary[trigtype](trigger_param)


def get_composite_trig_type(trigtype: str, trigger_param1, trigger_param2) -> Trigger:
    dictionary = {
        'AND': AndTrigger,
        'OR': OrTrigger,
    }
    return dictionary[trigtype](trigger_param1, trigger_param2)

SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Biden")
        t4 = AndTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
