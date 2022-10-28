from hashlib import md5
import json
from base64 import b64encode as b64

masks = "0,256"
encoding = "utf-8"

with open("mappings.data", "wb") as file:
    file.write(
            b64(
                json.dumps(
                    {str(x): md5(str(x).encode(encoding)).hexdigest() for x in range(
                        int(masks.split(",")[0]), 
                        int(masks.split(",")[1])
                    )}
                ).encode(encoding)
            )
        )
    file.close()