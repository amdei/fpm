from importlib_metadata import Distribution
import os
import sys
import pkg_resources
try:
    import json
except ImportError:
    import simplejson as json

PY3 = sys.version_info[0] == 3

if PY3:
    def u(s):
        return s
else:
    def u(s):
        if isinstance(u, unicode):
            return u
        return s.decode('utf-8')


# Note, the last time I coded python daily was at Google, so it's entirely
# possible some of my techniques below are outdated or bad.
# If you have fixes, let me know.


class get_metadata_toml():

    @staticmethod
    def run(output_path):
        dist = Distribution.at('.')
        data = {
            "name": dist.name,
            "version": dist.version,
            "author": ' '.join(dist.metadata.get_all('Author-email')),
            "description": dist.metadata['Summary'],
            "license": "FIXME!!!!",
            "url": ' '.join(dist.metadata.get_all('Project-URL')),
        }
# @todo FIXME!!!
#        if dist.metadata.has_ext_modules():
#            data["architecture"] = "native"
#        else:
#            data["architecture"] = "all"

        data["architecture"] = "all"

        final_deps = []

# @todo FIXME!!!
        data["dependencies"] = final_deps

        output = open(output_path, "w")
        if hasattr(json, 'dumps'):
            def default_to_str(obj):
                """ Fall back to using __str__ if possible """
                # This checks if the class of obj defines __str__ itself,
                # so we don't fall back to an inherited __str__ method.
                if "__str__" in type(obj).__dict__:
                    return str(obj)
                return json.JSONEncoder.default(self, obj)

            output.write(json.dumps(data, indent=2, default=default_to_str))
        else:
            # For Python 2.5 and Debian's python-json
            output.write(json.write(data))
        output.close()
