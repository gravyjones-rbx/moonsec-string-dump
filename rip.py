"""
The most bootleg string dump script ever made :3
any time we try to run a roblox script with standard lua it errors at some point
at this point theres always a local varible containing encoded data with plain text strings
we simply patch in some code to dump this varible to a file before the crash happens
"""

from urllib.parse import urlparse, parse_qs

import re
import sys
import os
import subprocess

ANTI_TAMPER_BYPASS = """
function deepcopy(orig)
	local orig_type = type(orig)
	local copy
	if orig_type == 'table' then
		copy = {}
		for orig_key, orig_value in next, orig, nil do
			copy[deepcopy(orig_key)] = deepcopy(orig_value)
		end
		setmetatable(copy, deepcopy(getmetatable(orig)))
	else -- number, string, boolean, etc
		copy = orig
	end
	return copy
end

local ourStringLib = deepcopy(string)
ourStringLib["match"] = function(a,b)
	if b == "%d+" then
		return "1"
	elseif b == ":%d+: a" then
		return ":1: a"
	end
	return string.match(a,b)
end

local oldgetfenv = getfenv
getfenv = function()
	t = oldgetfenv()
	local _t = t
	t = {}	
	local mt = {
		__index = function (t,k)
			if k == "string" then
				return ourStringLib
			end
			return _t[k]   -- access the original table
		end,
		__newindex = function (t,k,v)
			if k == "print" then
                return
            end
            if k == "tostring" then
                return
            end
            _t[k] = v 
		end
	}
	setmetatable(t, mt)
	return t
end
"""
VAR_DUMP = """
        for index=0,100 do
			local name, value = debug.getlocal(1, index)
			if type(value) == "string" and string.len(value) > 100 then 
				file = io.open("dumped_encoded_var", "w")
				file:write(value)
				file:close()
			end
		end
"""

def main():
    #open file
    with open("prettied_script.lua","r") as file:
        obfuscated_script = file.readlines()
        if len(obfuscated_script) < 1:
            print("[!] Script Not pretty :3")
            sys.exit(0)

    #add anti tamper
    #obfuscated_script.insert(0,ANTI_TAMPER_BYPASS) this fucks up the line count, but works otherwise
    ANTI_TAMPER_BYPASS_array = ANTI_TAMPER_BYPASS.split("\n")
    ANTI_TAMPER_BYPASS_array.reverse()
    for line in ANTI_TAMPER_BYPASS_array:
        obfuscated_script.insert(0,line+"\n")

        
    #find where error will occur
    error_magic1 = r"\\49.\\48'\)\)\s*~=\s*1"
    error_magic2 = r'return\s\(\w\s*\*\s*\w\)\s*\+\s*\(\w\s*\*\s*\w\)\s*\+\s*\(\w\s*\*\s*\w\)\s*\+\s*\w;'
    magic_pos = 0
    positive_locs = []
    for line in obfuscated_script:

        match1 = re.search(error_magic1,line)
        match2 = re.search(error_magic2,line)
        if match1 or match2:
            #insert var dump string
            positive_locs.append(magic_pos)
            #obfuscated_script.insert(magic_pos,VAR_DUMP)
            
        magic_pos = magic_pos + 1

    print("[!] error locations found at", positive_locs)
    index_counter = 0
    for pos in positive_locs:
        obfuscated_script.insert(pos-index_counter,VAR_DUMP)
	#index account was ment to be used but wasnt needed, can be removed

    with open("patched_script.lua","w") as file:
        file.write("".join(obfuscated_script))
    print("[!] Running script")

    retcode = subprocess.call(['lua', 'patched_script.lua'], 
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT)
    print(f"[!] ret code from lua is ... {retcode}!!")
    print("[!] Script should throw an error and it should've written a dump file :3")

    print("[!]extracting strings from dumped_encoded_var")
    with open("dumped_encoded_var", "r",encoding="utf-8",errors='ignore') as file:
        content = file.read()
        regex = r'([\_\-a-zA-Z0-9\/\.\:]*)'
        a = re.findall(regex, content)
        for i in a:
            #print any string
            #if len(i) > 1:
                #print(i)

            #print any url
            print_url(i,'')


            #print discord links
            #print_url(i,"discord.com")

            #print github links
            #print_url(i,"github")

def print_url(i,domain):
    parse = urlparse(i)
    if all([parse.scheme, parse.netloc]):
        if domain in parse.netloc:
            print(f"[!!]{domain} Url found (☞ﾟヮﾟ)☞ ",i)



if __name__ == "__main__":
    main()
