from flask import Flask, request, jsonify

app = Flask(__name__)

#Start data
tasks_list = [
    {"id": 0, "title": "First Task", "description": "complete and submit 5333 LAB2 on canvas"},
    {"id": 1, "title": "Second task", "description": "complete and submit 5333 inclass lab 2 on canvas "}
]


@app.route("/")
def hello():
   return "Hello world!!!"

# get tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks_list})

# get task by id
@app.route('/gettask/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((tasks_list for tasks_list in tasks_list if tasks_list['id'] == task_id), None)
    if task is not None:
        return jsonify({'task': task})
    else:
        return jsonify({'error': 'Task not found'}), 404
# create task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = {
        'id': len(tasks_list) + 1,
        'title': data['title'],
        'description': data['description']
    }
    tasks_list.append(new_task)
    return jsonify({'task': new_task}), 201

# update
@app.route('/updatetask/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((tasks_list for tasks_list in tasks_list if tasks_list['id'] == task_id), None)
    if task is not None:
        # save the data that is to be deleted
        old_title=task['title']
        old_description=task['description']
        data = request.get_json()
        task['title'] = data.get('title', task['title'])
        task['description'] = data.get('description', task['description'])
        return jsonify({'updated_task': task,'old_title':old_title,'old_description':old_description})
    else:
        return jsonify({'error': 'Task not found check id and try again'}), 404

# delete
@app.route('/tasksdelete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks_list
    tasks_list = [tasks_list for tasks_list in tasks_list if tasks_list['id'] != task_id]
    return jsonify({'result': True,'deleted taskid':task_id,'new todo list':tasks_list})

if __name__ == '__main__':
    app.run(debug=True)
