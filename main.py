import numpy as np
import pandas as pd
import string
import nltk
# this nltk.download('stopwords')
from nltk.corpus import stopwords
from datetime import datetime

import mysql.connector


from flask import Flask
from flask import Flask, request
app = Flask(__name__)


stopwords.words('english')
dataset1 = r"C:/Users/eslam/Desktop/Naive Bayes - 1/Naive Bayes - 1/PandNDataSet.csv"
table = pd.read_csv(dataset1)
negative = (table['neg'])
positive = (table['pos'])
dataset2 = r"C:/Users/eslam/Desktop/Naive Bayes - 1/Naive Bayes - 1/bad-words.csv"
table2 = pd.read_csv(dataset2)
bad = (table2['bad word'])
# print(positive)
# print("Enter the word :")

# splitting the words of the sentence into this list


@app.route("/ranking", methods=["POST"])
def ranking():
    comment = request.args.get('comment')
    user_id = request.args.get('user_id')
    movie_id = request.args.get('movie_id')
    comment = str(comment)
    user_id = int(user_id)
    movie_id = int(movie_id)
    
    print( comment,user_id,movie_id)
    comment_words_spllitted = comment.split()
    # the number of words in the comment
    comment_len = len(comment_words_spllitted)
    # Removing the stop words
    final_comment_list = []
    en_stops = set(stopwords.words('english'))
    for tockenized_comment in comment_words_spllitted:
        if tockenized_comment not in en_stops:
            final_comment_list.append(tockenized_comment)
            # print(tockenized_comment)
    # gprint("the words after clean :",final_comment_list)
    evaluation = 0

    cc = 0
    while cc < len(final_comment_list):
        ii = 0
        while ii < 4696:
            if final_comment_list[cc] == negative[ii]:
                evaluation = evaluation - 1
            ii += 1
        cc += 1
    c = 0
    while c < len(final_comment_list):
        i = 0
        while i < 4696:
            if final_comment_list[c] == positive[i]:
                evaluation = evaluation + 1
            i += 1
        c += 1
    lc = 0
    while lc < len(comment_words_spllitted):
        if comment_words_spllitted[lc] == "not":
            evaluation = evaluation * 0
        lc += 1
    ls = 0
    # while ls < len(final_comment_list):
    #     li = 0
    #     while li < 1616:
    #         if final_comment_list[ls] == bad[li]:
    #             evaluation = 111
    #         li += 1
    #     ls += 1

    # print(comment_words_spllitted)

    val = 0
    if evaluation > 0:
        val = 1

    if evaluation < 0:
        val = -1

    if evaluation == 0:
        val = 1

        # Connect to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="eslam",
        passwd="eslamelsoudy2001",
        database="recomendation-system"
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Define the data to insert

    value = val
    # Build the SQL query
    query = "INSERT INTO comments (movie_id, user_id, comment, value, created_at) VALUES (%s, %s, %s, %s, NOW())"

    cursor.execute(query, (movie_id, user_id, comment, value))

    # Execute the query with
    # Commit the changes
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return "done succesfuly", 200


if __name__ == '__main__':
    app.run()
