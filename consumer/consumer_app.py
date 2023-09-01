from flask import Flask, render_template, request
import requests
import json
import os

consumer = Flask(__name__)

API_TOKEN = dict()


API_host_url = os.getenv("GATEWAY_URL","http://localhost:8484")

@consumer.route("/")
def main():
    """Redirects a valid user to homepage otherwise to login page"""
    if request.form.get("user_name") not in API_TOKEN:
      return render_template("login.html")
    else:
      return render_template("list.html")

@consumer.route("/authorize", methods=["POST"])
def login():
    """Authorises a valid user and redirect to homepage"""
    token_response = requests.post(f'{API_host_url}/token', params={"username":request.form["user_name"],"password":request.form["password"]})
    if token_response.status_code == 200:
        API_TOKEN[request.form["user_name"]] = token_response.json()["access_token"]
        return list()
    else:
      return render_template("login.html", result=token_response.json()["detail"])

@consumer.route("/list", methods=["POST"])
def list():
    """Loads the homepage for valid users"""
    if API_TOKEN.get(request.form["user_name"]) is None:
      return render_template("login.html", result="Please login again.")
    else:
        resources_response = requests.get(f'{API_host_url}/api/resources', headers={"Authorization": "Bearer "+API_TOKEN[request.form["user_name"]]})
        if resources_response.status_code == 200:
          return render_template("list.html", resources=resources_response.json(),username=request.form["user_name"])

@consumer.route("/new_resource", methods=["POST"])
def show_resource_page():
    """Loads the new resource page for valid users"""
    if request.form.get("user_name") not in API_TOKEN:
      return render_template("login.html")
    else:
      return render_template("details.html",display_type="new",username=request.form["user_name"])

@consumer.route("/details", methods=["POST"])
def get_details():
    """Loads the detailed resource page for valid users"""
    if API_TOKEN.get(request.form["user_name"]) is None:
      return render_template("login.html", result="Please login again.")
    else:
        detail_response = requests.get(f'{API_host_url}/api/resources/'+request.form["resource_id"], headers={"Authorization": "Bearer "+API_TOKEN[request.form["user_name"]]})
        if detail_response.status_code == 200:
          return render_template("details.html", details=detail_response.json(),display_type="view",username=request.form["user_name"])
        return render_template("list.html", result=detail_response.json()["detail"],username=request.form["user_name"])

@consumer.route("/add_details", methods=["POST"])
def add_details():
    """Adds new resource and loads the detailed resource page for valid users """
    if API_TOKEN.get(request.form["user_name"]) is None:
      return render_template("login.html", result="Please login again.")
    else:
        resource = {}
        resource['id'] = int(request.form["resource_id"])
        resource['name'] = request.form["resource_name"]
        resource['type'] = request.form["resource_type"]
        resource['is_endangered'] = bool(request.form["is_endangered"])
        json_resource = json.dumps(resource)
        
        detail_response = requests.post(f'{API_host_url}/api/resources/'+request.form["resource_id"], headers={"Authorization": "Bearer "+API_TOKEN[request.form["user_name"]]}, json=json.loads(json_resource))
        if detail_response.status_code == 201:
          return render_template("details.html", details=detail_response.json(),display_type="view",username=request.form["user_name"])
        return render_template("details.html", result=detail_response.json()["detail"],username=request.form["user_name"])

@consumer.route("/update_resource", methods=["POST"])
def update_resource_page():
    """Loads the update resource page for valid users"""
    if API_TOKEN.get(request.form["user_name"]) is None:
      return render_template("login.html", result="Please login again.")
    else:
        detail_response = requests.get(f'{API_host_url}/api/resources/'+request.form["resource_id"], headers={"Authorization": "Bearer "+API_TOKEN[request.form["user_name"]]})
        if detail_response.status_code == 200:
          return render_template("details.html", details=detail_response.json(),display_type="update",username=request.form["user_name"])
        return render_template("list.html", result=detail_response.json()["detail"],username=request.form["user_name"])


@consumer.route("/update_details", methods=["POST"])
def update_details():
    """Updates given resource and loads the detailed resource page for valid users """
    if API_TOKEN.get(request.form["user_name"]) is None:
      return render_template("login.html", result="Please login again.")
    else:
        resource = {}
        resource['id'] = int(request.form["resource_id"])
        resource['name'] = request.form["resource_name"]
        resource['type'] = request.form["resource_type"]
        resource['is_endangered'] = bool(request.form["is_endangered"])
        json_resource = json.dumps(resource)

        detail_response = requests.put(f'{API_host_url}/api/resources/'+request.form["resource_id"], headers={"Authorization": "Bearer "+API_TOKEN[request.form["user_name"]]}, json=json.loads(json_resource))
        if detail_response.status_code == 200:
          return render_template("details.html", details=detail_response.json(),display_type="view",username=request.form["user_name"])
        return render_template("details.html", result=detail_response.json()["detail"],username=request.form["user_name"])

@consumer.route("/delete_details", methods=["POST"])
def delete_details():
    """Deletes given resource for valid users """
    if API_TOKEN.get(request.form["user_name"]) is None:
      return render_template("login.html", result="Please login again.")
    else:
        detail_response = requests.delete(f'{API_host_url}/api/resources/'+request.form["resource_id"], headers={"Authorization": "Bearer "+API_TOKEN[request.form["user_name"]]})
        if detail_response.status_code == 204:
          return render_template("details.html",username=request.form["user_name"])
        
        return render_template("details.html", result=detail_response.json()["detail"],username=request.form["user_name"])

@consumer.route("/logout", methods=["POST","GET"])
def logout():
    """Logs out the user and redirects to login page"""
    if request.form.get("user_name") in API_TOKEN:
        API_TOKEN.pop(request.form["user_name"])
    return render_template("login.html")
     
@consumer.errorhandler(404)
@consumer.errorhandler(405)
def not_found(error):
    """Redirects to 400 series error page"""
    return render_template("40x.html", error=error)

@consumer.errorhandler(500)
def server_error(error):
    """Redirects to server error page"""
    return render_template("500.html", error=error)
