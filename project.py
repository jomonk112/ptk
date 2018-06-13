from flask import Flask,render_template,request,session,redirect,url_for
from flask import jsonify
from connection import connection

app = Flask(__name__)
app.secret_key="asdfghj"
c=[]

#@app.route('/')
#def hello_world():
 #   return 'Hello World!'
@app.route('/')
def ll():
    return render_template('login.html')

@app.route('/register')
def reg():
    return render_template('user.html')

@app.route('/user_register',methods=['post'])
def user_registers():
    name=request.form['name']
    place=request.form['place']
    phone=request.form['phone']
    email=request.form['email']
    user=request.form['user']
    pswd=request.form['pswd']
    s="insert into user(name,place,phone,email) values('"+name+"','"+place+"','"+phone+"','"+email+"')"
    ss="insert into login(username,password,type) values('"+user+"','"+pswd+"','user')"
    cur,conn=connection()
    cur.execute(s)
    cur.execute(ss)
    conn.commit()
    return render_template('login.html')


@app.route('/add')
def add_prdct():
    sql = "select * from category"
    cur, conn = connection()
    cur.execute(sql)
    res = cur.fetchall()
    return render_template('/product.html',d=res)
@app.route('/cat')
def ctgry_add():
    s="select * from category"
    cur,conn=connection()
    cur.execute(s)
    res=cur.fetchall()
    return render_template('/category.html',s=res)

@app.route('/add_p',methods=['post'])
def prdct():
    name=request.form['pname']
    sql="insert into category(category) VALUES ('"+name+"')"
    cur,conn=connection()
    cur.execute(sql)
    conn.commit()
    s="select * from category"
    #a1,a2=cont()
    cur.execute(s)
    res=cur.fetchall()
    return render_template('category.html',s=res)
@app.route('/prdct',methods=['post'])
def p_add():

    sq="select max(pid) from product"
    cur,conn=connection()
    cur.execute(sq)
    res=cur.fetchone()
    if res is not  None:
        mid=res[0]+1
    else:
        mid=0

    img = request.files['img']
    img.save("C:\\Users\\babbu\\PycharmProjects\\project\\static\\image\\" + str(mid) + ".png")
    path = ("./static/image/" +str(mid) + ".png")

    name=request.form['product']
    price=request.form['price']
    category=request.form['category']
    s="insert into product(pname,price,image,cid) values('"+name+"','"+price+"','"+path+"','"+category+"')"
    s1,s2=connection()
    s1.execute(s)
    s2.commit()

    return "product added"

@app.route('/display')
def dis():
    s="select * from product"
    s1,s2=connection()
    s1.execute(s)
    res=s1.fetchall()
    return render_template('view.html',d=res)



@app.route('/login',methods=['post'])
def log1():
    user=request.form['user']
    paswd=request.form['pswd']
    s="select * from login where username='"+user+"' and password='"+paswd+"'"
    cur,conn=connection()
    cur.execute(s)
    result=cur.fetchone()

    if result is not None:
        if result[3]=='user':
            session["id"] = result[0]
            return redirect(url_for('user_home'))
            #return user_home()
            #s = "select * from category"
            #cur, conn = connection()
            #cur.execute(s)
            #res = cur.fetchall()
            #return render_template('userhome.html', r=res)
            #result=user_home()
        elif result[3]=='admin':
            return hm()
        else:
            return render_template('user.html')

    else:
        return render_template('user.html')

@app.route('/del/<id>')
def dlt(id):
    s="delete from category where cid='"+id+"'"
    s1,s2=connection()
    s1.execute(s)
    s2.commit()
    return ctgry_add()
@app.route('/view/<id>')
def show(id):
    s="select pname,price,image from product where cid='"+id+"'"
    s1,s2=connection()
    s1.execute(s)
    s2.commit()
    res=s1.fetchall()
    return render_template('pro_list.html',d=res)

@app.route('/search')
def data():
    val = request.args.get("b")
    #val=request.form['b']
    print(val)

    s="select * from product where pname like '"+val+"%'"
    cur,conn=connection()
    cur_count=cur.execute(s)
    print(cur_count)
    if cur_count>0:
    #conn.commit()\
        res = cur.fetchall()
    #  print(res)
   # if res is not None:
        row_header = [x[0] for x in cur.description]
        json_data = []
        for result in res:
            json_data.append(dict(zip(row_header, result)))
        print(json_data)
        return jsonify(json_data)
    else:
        print("hjhj")
        category="select cid from category where category like '"+val+"%'"
        cur.execute(category)
        c_id=cur.fetchone()
       # str (c_id[0])
        #print (type(c_id))
        if c_id is None:
            return render_template(status="no item found")
        else:
            product="select * from product where cid='"+str(c_id[0])+"'"
            cur.execute(product)
            prdct=cur.fetchall()
            print(prdct)
            if prdct is not None:
                row_header = [x[0] for x in cur.description]
                json_data = []
                for result in prdct:
                    json_data.append(dict(zip(row_header, result)))
                print(json_data)
                return jsonify(json_data)

@app.route('/home')
def hm():
    return render_template('home.html')

@app.route('/userhome')
def user_home():
    s="select * from category"
    cur,conn=connection()
    cur.execute(s)
    res=cur.fetchall()
    return render_template('userhome.html', r=res)

@app.route('/checks')
def checkk():
    res=[]
    c_id=request.args.get("category")
   # searchs=request.args.get("value")
    #print(searchs)
    print(c_id)
    for i in c_id:
        s = "select  * from product where cid='" + i + "' "
        cur, conn = connection()
        cur.execute(s)
        res.extend(cur)
    print("inside check",res)
    row_header = [x[0] for x in cur.description]
    json_data = []
    for result in res:
        json_data.append(dict(zip(row_header, result)))
        print(json_data)
    return jsonify(json_data)

@app.route('/add_cart/<id>')
def adds(id):
    print(id)
    #print(list(c))
    uid=str(session["id"])
    s="insert into cart(pid,uid) values('"+id+"','"+uid+"')"
    cur,conn=connection()
    cur.execute(s)
    conn.commit()
    d="select * from category"
    cur.execute(d)
    category=cur.fetchall()
    return render_template('userhome.html',r=category)
@app.route('/shop')
def shp():
    uid=str(session["id"])
    s="select product.pid,product.pname,product.image,product.price from product inner join cart on product.pid=cart.pid and cart.uid='"+uid+"'"
    s1,s2=connection()
    s1.execute(s)
    res=s1.fetchall()
    print(res)
    total=0
    for i in res:
        total=total+i[3]
    print(total)
    return render_template('order.html', n=res, p=total)

@app.route('/remove/<id>')
def rmv(id):
    uid=str(session["id"])
    s="delete from cart where uid='"+uid+"' and pid='"+id+"'"
    s1,s2=connection()
    s1.execute(s)
    s2.commit()
    return redirect(url_for('shp'))

@app.route('/userr')
def use():
    return render_template('userhome.html')


@app.route('/search2')
def data1():
    item = request.args.get("value")
    lists= request.args.get("lists")
    res=[]
    selected_data=tuple(lists)
    print("jbj",selected_data)
    for i in selected_data:
        s = "select  * from product where cid='" + i + "'"
        cur, conn = connection()
        cur.execute(s)
        res.extend(cur)
    print("mmlmlm",res)
    length=len(res)
    print(length)
    result=[]
    for i in range(0,length):
        print(i)
        for j in range(res[0][4]):
            product="select * from product where pname like '"+item+"%' and cid='"+str(res[i][j])+"' group by pname"
            cur,conn=connection()
            cur.execute(product)
            result.extend(cur)
    print(result)
    if result is not None:
        row_header=[x[0] for x in cur.description]
        json_data=[]
        for results in result:
            json_data.append(dict(zip(row_header,results)))
        print (json_data)
        return jsonify(json_data)

    else:
        return "no match found"


if __name__ == '__main__':
    app.run()