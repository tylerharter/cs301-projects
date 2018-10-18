import re

state_file = ".state.json"
macro_file = "macros.txt"
repo_dir = "repo"
review_dir = "reviews"
submissions_dir = "submissions"
signin_url = "https://tyler.caraza-harter.com/cs301/fall18/reviewer.html"
review_prefix = "#%"
repo_link = "https://github.com/tylerharter/cs301-projects.git"
aws_cred_profile = 'cs301ta'
s3_bucket = 'caraza-harter-cs301'
cs301_lambda_endpoint = "https://1y4o8v9snh.execute-api.us-east-2.amazonaws.com/default/cs301"
fn_list_submissions = "project_list_submissions"
fn_put_code_review = "put_code_review"

deduct_keyword = "DEDUCT"
deduct_regex = re.compile("^.*DEDUCT (?P<score>\d+).*$")
macro_keyword = "#define"

# environ keywords
tacli_token_env = "TACLI_TOKEN"
tacli_editor_env = "TACLI_EDITOR"
tacli_difftool_env = "TACLI_DIFFTOOL"
