from jinja2 import *
import yaml
import logging


def jina_template_loader(filepath, filename):
    # This loads the Jina2 template
    j2_env = Environment(loader=FileSystemLoader('{}'.format(filepath)),
                         trim_blocks=True)
    jinja_template = j2_env.get_template('{}'.format(filename))
    return jinja_template


def yaml_loader(filepath):
    # Loads the variable data yaml file
    with open(filepath, "r") as y:
        data = yaml.load(y, yaml.FullLoader)
    return data


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        filename='app.log',
                        filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')
    logging.info("0/1: --------- Starting Config Generation Script!")
    jinja_template_filepath = 'templates'
    jinja_template_filename = 'template.j2'
    yaml_filepath = 'input_data.yaml'
    template = jina_template_loader(
        jinja_template_filepath, jinja_template_filename)
    input_data = yaml_loader(yaml_filepath)
    logging.info("0/2: Processing YAML File to build inventory ")
    for k, v in input_data.items():
        if v is None:
            logging.error("\n\n\n0/2: ERROR: YAML file contains missing "
                          "variables, please complete and run the script "
                          "again.\n\n\n")
            exit()
    rendered_template = template.render(input_data=input_data)
    logging.info("0/3: Processing 'template.j2' Template ")
    f = open(
        'generated_config_files/{}_configuration.txt'
        .format(input_data['site_name']), 'w')
    logging.info(
        "0/4: Generating 'generated_config_files/{}_configuraiton.txt' file"
        .format(input_data['site_name']))
    f.write(rendered_template)
    f.close()
    logging.info("0/5: --------- Complete! Configs in "
                 "'generated_config_files'")
