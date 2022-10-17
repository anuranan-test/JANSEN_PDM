import hashlib
import config

class hashing:
    for col in df.values.tolist():
      df[col.strip()] = df[col.strip()].apply(
                      lambda x: '0x' + hashlib.md5((str(x)+str(salt)).encode()).hexdigest().upper())
