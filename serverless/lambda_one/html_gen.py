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


                {}

                <form name="input_box">
                    <h1></h1>
                    <input type="text" name="phonenumber-input" placeholder="enter number e.g 27842342354">
                    <input name="" type="button" value="Add">
                    <input name="" type="button" value="Send" onclick="myFunction()">
                </form>

                <script>
                        function myFunction() {{
                            var x = document.getElementsByClassName("chip");
                            alert("detected " + x.length + " numbers.");
                        }}
                </script>
                </body>
                </html>"""

def generate_chips(contacts):
    """Generates html chips from a list of contact numbers"""
    chips = ""
    for contact in contacts:
        chip = """<div class="chip">
                %s
                <span class="closebtn" onclick="this.parentElement.style.display='none'">&times;</span>
                </div>""" % contact
        chips += chip
    return template.format(chips)