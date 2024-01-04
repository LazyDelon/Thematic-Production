from flask import Flask, request, render_template
  
  
app = Flask(__name__)
  
  
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        languages = []

        with open('stock_number.csv', encoding="utf-8") as f: 
            slist = f.readlines() 
            for lst in slist: 
                s = lst.split(',') 
                
                # languages.append('{}'.format(s[0].strip()))
                # languages.append('{}'.format(str(s[1].strip())))
                languages.append('{} {}'.format(s[0].strip(),str(s[1].strip())))
                
    return render_template("home.html", languages=languages)
  
  
if __name__ == '__main__':
    app.run(debug=True)