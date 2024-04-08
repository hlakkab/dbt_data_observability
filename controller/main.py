import json
from flask import Flask, jsonify, request
from entities.FreshnessTest import FreshnessTest
from service.FreshnessTestService import generate_yaml_file_for_freshness_test, generate_dag_based_on_freshness_test
app = Flask(__name__)

employees = [
    {'id': 1, 'name': 'Ashley'},
    {'id': 2, 'name': 'Kate'},
    {'id': 3, 'name': 'Joe'}
]

nextEmployeeId = 4


@app.route('/', methods=['GET'])
def get_employees():
    return jsonify(employees)


@app.route('/employees/<int:id>', methods=['GET'])
def get_employee_by_id(id: int):
    employee = get_employee(id)
    if employee is None:
        return jsonify({'error': 'Employee does not exist'}), 404
    return jsonify(employee)


def get_employee(id):
    return next((e for e in employees if e['id'] == id), None)


tests = [
    FreshnessTest("Test 1", "daily", "users"),
    FreshnessTest("Test 2", "weekly", "users"),
    FreshnessTest("Test 3", "daily", "users"),
    FreshnessTest("Test 4", "weekly", "users"),
]


# Controller with API Endpoint
@app.route('/api/tests', methods=['GET'])
def get_tests():
    # Return all tests
    return jsonify([{'name': test.name, 'type': test.frequency} for test in tests])


@app.route('/api/create_test', methods=['POST'])
def create_test():
    data = request.get_json()
    name = data.get('name')
    frequency = data.get('frequency')
    table_name = data.get('table_name')
    new_test = FreshnessTest(name, frequency, table_name)
    generate_yaml_file_for_freshness_test(table_name, "1" , ho)
    tests.append(new_test)

    return jsonify([{'name': test.name, 'type': test.frequency} for test in tests])


if __name__ == '__main__':
    app.run(port=5000)
