from flask import Flask, render_template, request

import numpy as np
import random

app = Flask(__name__)

block_data = []
clear = False

@app.route("/")
def index():
  index=['hello','todoApp','right_out']
  return render_template('index.html',index=index)

@app.route('/hello')
def hello():
  greeting='HELLO!'
  names=['Matsudo','Kashiwa','Abiko']
  return render_template('hello.html',greeting=greeting,name=np.random.choice(names))

todos = []

@app.route('/todoApp', methods=['GET','POST'])
def todoApp():
  if request.method == 'GET':
    return render_template('todoApp.html',todos=todos)
  
  if request.method == 'POST':
    if 'add' in request.form.keys():
      value = request.form['add']
      if value != "":
        if value not in todos:
          todos.append(value)
      return render_template('todoApp.html',todos=todos)

    if 'remove' in request.form.keys():
      value2 = request.form['remove']
      if value2 in todos:
        todos.remove(value2)
      return render_template('todoApp.html',todos=todos)


@app.route('/right_out', methods=['GET','POST'])
def right_out():
  if request.method == 'GET':
    return render_template('right_out.html',block_data=block_data)

  if request.method == 'POST':
    if "num" in request.form.keys():
      block_size = request.form["num"]
      for i in range(int(block_size)):
        line_data = []
        for j in range(int(block_size)):
          line_data.append(random.choice([True, False]))
        block_data.append(line_data)
      return render_template('right_out.html',block_data=block_data)

    if "block" in request.form.keys():
      block_info = request.form["block"]
      # 出力方法 下
      app.logger.debug(block_info) 

      block_list = block_info.split('$')
      block_num = len(block_data)
      block_data[int(block_list[0])][int(block_list[1])] = not(block_data[int(block_list[0])][int(block_list[1])])
      if block_num - int(block_list[0]) > 1:
        block_data[int(block_list[0])+1][int(block_list[1])] = not(block_data[int(block_list[0])+1][int(block_list[1])])
      if block_num - int(block_list[0]) < block_num:
        block_data[int(block_list[0])-1][int(block_list[1])] = not(block_data[int(block_list[0])-1][int(block_list[1])])
      if block_num - int(block_list[1]) > 1:
        block_data[int(block_list[0])][int(block_list[1])+1] = not(block_data[int(block_list[0])][int(block_list[1])+1])
      if block_num - int(block_list[1]) < block_num:
        block_data[int(block_list[0])][int(block_list[1])-1] = not(block_data[int(block_list[0])][int(block_list[1])-1])

      clear = True
      for i in range(len(block_data)):
        for j in block_data[i]:
          if j:
            clear = False
      return render_template('right_out.html',block_data=block_data,clear=clear)
    
    if "reset" in request.form.keys():
      block_data.clear()
    return render_template('right_out.html',block_data=block_data)




if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')
