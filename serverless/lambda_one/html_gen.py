template = """<!DOCTYPE html>
				<html>
					<head>
					<meta name="viewport" content="width=device-width, initial-scale=1">
						<style>
						.chip {{
						  display: inline-block;
						  padding: 0 25px;
						  height: 50px;
						  font-size: 18px;
						  line-height: 50px;
						  border-radius: 25px;
						  background-color: #1f2e2e;
						}}

						.chip img {{
						  float: left;
						  margin: 0 10px 0 -25px;
						  height: 50px;
						  width: 50px;
						  border-radius: 50%;
						}}

						.closebtn {{
						  padding-left: 10px;
						  color: #888;
						  font-weight: bold;
						  float: right;
						  font-size: 20px;
						  cursor: pointer;
						}}

						.closebtn:hover {{
						  color: #000;
						}}

						h3 {{ 
						  color: #888;
						  font-family: Verdana, Geneva, Tahoma, sans-serif 
						}}

						input {{   
						  padding: 0 25px;
						  height: 50px;
						  font-size: 18px;
						  line-height: 50px;
						  border-radius: 25px;
						  background-color: #1f2e2e; 
						  border: #1f2e2e;
						}}
						</style>
					</head>
				<body bgcolor="#0a0f0f">
				    <h3>Welcome. Please enter numbers to be processed.</h3>
				    <h3>If you are happy with your default numbers, click send.</h3>
				    <div id="user_id" data-user-id="{0}"></div>

				{1}

				  <form name="input_box">
				      <h1></h1>
				      <input type="text" id="number-input" placeholder="enter number e.g 27842342354" pattern="^((?:27|27)|27)(=60|61|62|63|64|65|66|67|68|70|71|72|73|74|75|76|77|78|79|81|82|83|84|85|86|87)(\\d{{7}})$" required>
				      <input name="" type="button" value="Add" onclick="generateChip()">
				      <input id="send" type="button" value="Send" onclick="sendToServer()">
				  </form>

				  <script>
              const generateChip = () => {{
                  var user_input = document.getElementById("number-input").value;
                  let pattern = /^((?:27|27)|27)(=60|61|62|63|64|65|66|67|68|70|71|72|73|74|75|76|77|78|79|81|82|83|84|85|86|87)(\d{{7}})$/;
                  var is_valid = pattern.test(user_input);
                  if (is_valid) {{
                      var space = document.createElement("p");
                      document.body.appendChild(space);
                      var new_chip = document.createElement("div");
                      guid = (S4() + S4() + "-" + S4() + "-4" + S4().substr(0,3) + "-" + S4() + "-" + S4() + S4() + S4()).toLowerCase();
                      new_chip.id = guid;
                      new_chip.className = "chip";
                      new_chip.textContent = user_input;
                      document.body.appendChild(new_chip);
                      document.getElementById(guid).innerHTML += '<a href="https://ibb.co/KV6LZx5"><img src="https://i.ibb.co/KV6LZx5/img-avatar.jpg" alt="" width="96" height="96"></a><span class="closebtn" onclick="this.parentElement.style.display=\\'none\\'; this.parentElement.textContent=\\'\\'">&times;</span>';
                  }}
              }};

				        function S4() {{
				            return (((1+Math.random())*0x10000)|0).toString(16).substring(1); 
				        }};

				        document.getElementById("send").onclick = function () {{
				            let chip_values = document.getElementsByClassName("chip");
				            let numbers = [];
				            for (x=0; x < chip_values.length; x++) {{
                        if (chip_values[x].textContent != '') {{
				                    numbers.push(chip_values[x].textContent
				                     .replace(/[\\n\\r]+|[\\s]{{2,}}/g, ' ').replace(/\\D/g, '').trim());
												}}
				            }};
										if (numbers.length > 0) {{
												let div = document.getElementById("user_id");
												let user_id = div.getAttribute("data-user-id");
												let base_path = "https://wppfmzs7bd.execute-api.us-east-1.amazonaws.com/dev/get_qr?";
												let path_params = `user=${{user_id}}&data=[${{numbers}}]`;
												alert(base_path + path_params);
												location.href = base_path + path_params;
										}}
										else {{
											  alert('Please enter at least one number to be processed.');
										}};
				        }};
				  </script>

				</body>
				</html>"""

def generate_chips(user, contacts):
    """Generates html chips from a list of contact numbers"""
    chips = ""
    for contact in contacts:
        chip = """<div class="chip">
                <a href="https://ibb.co/KV6LZx5"><img src="https://i.ibb.co/KV6LZx5/img-avatar.jpg" alt="" width="96" height="96"></a>
                %s
                <span class="closebtn" onclick="this.parentElement.style.display='none'; this.parentElement.textContent=''">&times;</span>
                </div>""" % contact
        chips += chip
    return template.format(user, chips)