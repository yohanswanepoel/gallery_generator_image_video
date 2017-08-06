import webbrowser
import os
import sys, getopt
from os.path import isfile, join

BGCOLORHEX = "#202020"
BGCOLOR = "style=\"background-color:%s\"" %BGCOLORHEX
PAGES = [
    {"link":"imglist.html","name":"Photos","type":"img","path":"img"},
    {"link":"shortlist.html","name":"Trailers","type":"vid","path":"short"},
    {"link":"fulllist.html","name":"Full Videos","type":"vid","path":"tv"},
    ]
INDEX_LINK = "index.html"
INDEX_CONTENT = """
    <h3>What this is about</h3>
    <div class="row ">
    <p>
    Photos and videos from our holiday <br>
    </p>
    </div>"""
SITE_NAME = "Holiday Snaps"

def main(argv):
    nav_bar = generate_nav_bar(INDEX_LINK,SITE_NAME,PAGES)  #Generates the nav bar to link to pages
    page_head = genereate_head(nav_bar)  #Generates the page head content including the NavBar
    generate_pages(PAGES,page_head) #Generates the pages containing images and videos
    generate_index(INDEX_LINK,page_head,INDEX_CONTENT) #Generates the index.html

def generate_pages(pages, page_head):
    for page in pages:
        generate_page(page["path"],page["link"],page["type"],page_head)

def genereate_head(navigation_bar):
    page_head = """<!doctype html>
    <html>
        <head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/galleria/1.5.7/galleria.min.js"></script>

            <style>
                .listScroll {
                  height:600px;
                  overflow-y: scroll;
                }
                .galleria{ max-width: 1000px; height: 600px; background: %s}
            </style>
        </head>
        <body %s>
            %s
            """ % (BGCOLORHEX,BGCOLOR,navigation_bar)
    return page_head

def generate_page(input_directory,output_file_name,content_type,page_header):
    path=input_directory
    cwd = os.getcwd()
    content_path = cwd + "/" + path
    output_file = open(output_file_name,'w')
    # Scans the path and ignores hidden files and directories Only works one deep
    files = [f for f in os.listdir(content_path) if(isfile(join(content_path,f)) and not f.startswith(".")) ]
    if content_type == "img":
        file_content = generate_images_page(files,path,page_header)
    elif content_type == "vid":
        file_content = generate_videos_page(files,path,page_header)
    else:
        print("Invalid Content Type specify img or vid only")
    output_file.write(file_content)
    output_file.close
    print ("Done Generated File", output_file_name)

def generate_nav_bar(index_link, site_name, nav_links):
    nav_head="""<nav class="navbar navbar-toggleable-md navbar-inverse " style="background-color: #101010;">

              <a class="navbar-brand text-danger" href="%s">%s</a>

              <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">""" %(index_link, site_name)
    nav_content = ""
    for l in nav_links:  #Iterate through pages to get links
        nav_content += """
                  <li class="nav-item">
                    <a class="nav-link" href="%s">%s</a>
                  </li>
                  """ % (l["link"],l["name"])

    nav_tail =   """    </ul>
              </div>
            </nav>"""
    return nav_head + nav_content + nav_tail

def generate_index(output_file_name,page_head, content):

    cwd = os.getcwd()

    output_file = open(output_file_name,'w')

    page_content ="""<div class="container">
    <div class="container text-muted">
        <br>

            %s

    </div>
    </div>
        </body>
    </html>""" % content
    file_content = page_head + page_content
    output_file.write(file_content)
    output_file.close
    print ("Done Generated File", output_file_name)

def generate_videos_page(files,path,page_head):
    local_head = """
            <div class="container">
                <div class="row">
                    <div class="col">

                        <iframe name="player" id="player" height="600" width="700" style="border:.5px solid grey;"></iframe>
                    </div>
                    <div class="col">
                        <div class="list-group listScroll "> """
    local_body = ""
    for f in files:
        local_body += """ <a href="%s/%s" style="font-size:8pt" class="list-group-item list-group-item-action bg-inverse text-muted" target="player"> %s </a>""" % (path, f, f)

    local_tail ="""        </div>
                    </div>

                </div>
            </div>
            <script src="https://code.jquery.com/jquery-3.1.1.slim.min.js" integrity="sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bo
        </body>
    </html>"""
    return page_head + local_head + local_body + local_tail

def generate_images_page(files,path,page_head):
    local_head = """
            <div class="container">
            <div class="galleria">"""
    local_body = ""
    for f in files:
        local_body += """ <img src="%s/%s"> """ % (path, f)

    local_tail ="""        </div>
            <div>
            <script>

    	(function() {
                Galleria.loadTheme('https://cdnjs.cloudflare.com/ajax/libs/galleria/1.5.7/themes/classic/galleria.classic.min.js');
                Galleria.run('.galleria');
            }());
            </script>
        </body>
    </html>"""
    return page_head + local_head + local_body + local_tail

if __name__ == "__main__":
   main(sys.argv[1:])
