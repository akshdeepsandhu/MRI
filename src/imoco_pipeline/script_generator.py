import os
import logging

class ScriptGenerator:
    def __init__(self, scratch_path, h5_file_name, scan_id):
        self.scratch_path = scratch_path
        self.h5_file_name = h5_file_name
        self.scan_id = scan_id

    def generate_script(self, template_path, script_path, replacements):
        try:
            with open(template_path, 'r') as template_file:
                template_content = template_file.read()

            for placeholder, value in replacements.items():
                template_content = template_content.replace(placeholder, value)

            with open(script_path, 'w') as script_file:
                script_file.write(template_content)

            os.chmod(script_path, 0o755)
            logging.info(f"Script generated at {script_path}")
        except IOError as e:
            logging.error(f"Error handling template file: {e}")
            raise

    def generate_preprocess_script(self, script_path):
        self.generate_script(
            template_path='preprocess_template.sh',
            script_path=script_path,
            replacements={
                '{SCRATCH_PATH}': self.scratch_path,
                '{H5_FILE_NAME}': self.h5_file_name
            }
        )

    def generate_imoco_script(self, script_path):
        self.generate_script(
            template_path='imoco_termplate.sh',
            script_path=script_path,
            replacements={
                '{SCRATCH_PATH}': self.scratch_path,
                '{SCAN_ID}': self.scan_id
            }
        )
