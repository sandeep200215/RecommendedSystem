from flask import Flask,render_template,request
import pandas as pd
import numpy as np;
import pickle;
popular_pdf=pd.read_pickle("popular.pkl")
pt=pd.read_pickle("pt.pkl")
books=pd.read_pickle("books.pkl")
similarity_score=pd.read_pickle("similarity_scores.pkl")
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_pdf['Book-Title'].values),
                           author=list(popular_pdf['Book-Author'].values),
                           image=list(popular_pdf['Image-URL-M'].values)
                           )
@app.route("/recommend")
def recommend_ui():
     return render_template("recommend.html")
@app.route("/recommend_books",methods=['post'])
def recommend_bokks():
      user_input=request.form.get('user_input')
      index=np.where(pt.index==user_input)[0][0]
      similar_items=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:5]
      data=[]
      for i in similar_items:
          items=[];
          temp_df = books[books['Book-Title'] == pt.index[i[0]]]
          items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
          items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
          items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

          data.append(items)
          print(data)
      return  render_template("recommend.html",data=data)
if __name__=='__main__':
      app.run(debug=True)






