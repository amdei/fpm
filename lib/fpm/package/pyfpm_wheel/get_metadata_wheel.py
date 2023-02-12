import os
import sys
from pkginfo import Wheel

import json

# If you have fixes, let me know.

class get_metadata_wheel:
    wheel_path = None

    def __init__(self, wheel_path):
        self.wheel_path = wheel_path

    def get_home_url(self, project_urls):
        res = dict([i.strip() for i in x.split(',')] for x in project_urls)
        return res.get('Home', None)

    def run(self, output_path):

        fpm_wheel = Wheel(self.wheel_path)
        data = {
            "name": fpm_wheel.name,
            "version": fpm_wheel.version,
            "description": fpm_wheel.summary,
            "license": fpm_wheel.license,
        }

        if fpm_wheel.author:
            data["author"] = "%s <%s>" % (fpm_wheel.author, fpm_wheel.author_email)
        else:
            data["author"] = "%s" % (fpm_wheel.author_email)

        if fpm_wheel.home_page:
            data["url"] =  fpm_wheel.home_page
        else:
            data["url"] =  self.get_home_url(fpm_wheel.project_urls)

        # @todo FIXME!!!
        if fpm_wheel.requires_external:
            data["architecture"] = "native"
        else:
            data["architecture"] = "all"

        print('REQ:', fpm_wheel.requires, file=sys.stderr)
        print('REQ DIST:', fpm_wheel.requires_dist, file=sys.stderr)

        final_deps = []

# @todo FIXME!!!
        data["dependencies"] = final_deps

        with open(output_path, "w") as output:
            def default_to_str(obj):
                """ Fall back to using __str__ if possible """
                # This checks if the class of obj defines __str__ itself,
                # so we don't fall back to an inherited __str__ method.
                if "__str__" in type(obj).__dict__:
                    return str(obj)
                return json.JSONEncoder.default(self, obj)

            output.write(json.dumps(data, indent=2, sort_keys=True, default=default_to_str))
