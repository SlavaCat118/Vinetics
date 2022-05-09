import random
import fileManager as file
import pprint

def mapPreset(path):
	def mapTbl(tbl, head):
		retTbl = {}
		for i in tbl:
			if type(tbl[i]) != dict:
				retTbl[i] = head + [i]
			else:
				if i != "sample":
					head = head + [i]
					for j in mapTbl(tbl[i], head):
						retTbl[j] = head + [j]
					head.pop()
		return retTbl
	return mapTbl(file.openJson(path), [])

def nestGet(dic, keys):
	for i in keys:
		dic = dic[i]
	return dic

def nestSet(dic, keys, value):
	for i in keys[:-1]:
		if type(dic) == dict:
			dic = dic.setdefault(i, {})
		else:
			dic = dic[i]
	dic[keys[-1]] = value

# Actually useful stuff

def scaleRange(newMin, newMax, vals):
	return [((i-min(vals))*(newMax-newMin))/(max(vals)-min(vals)) for i in vals]

def scaleToPercent(vals):
	return scaleRange(0,100, vals + [0, sum(vals)])[0:-2]

def breed(baseParent, parentSettings, offspring, path, crossProb):

	print("Generating...")

	maps = file.openJson("dictionaryRemap.json")
	objs = {}
	weights = {}

	for i in parentSettings:
		name = file.baseName(i[1])
		weights[name] = i[0]
		objs[name] = file.openJson(i[1])


	weightKeys = list(weights.keys())
	objKeys = list(objs.keys())

	weightList = []
	for i in weightKeys:
		weightList.append(float(weights[i]))

	weightList = scaleToPercent(weightList)

	for n, i in enumerate(weightKeys):
		weights[i] = weightList[n]

	descriptions = []
	names = []
	errors = ""

	for i in range(offspring):
		description = ""
		used = {}
		base = file.openJson(baseParent)

		for i in maps:

			if random.randrange(0,100) <= crossProb:
				sucess = False
				iterations = 0
				while sucess == False and iterations < len(objKeys):
					keyUsed = random.choices(weightKeys, weightList)[0]
					used[keyUsed] = used.get(keyUsed, 0) + 1
					try:
						nestSet(base, maps[i], nestGet(objs[keyUsed], maps[i]))
						sucess = True
					except KeyError:
						errors += "\nKey: " + i + " not in " + keyUsed
						iterations += 1
				if iterations > len(objKeys):
					errors += "\nParents didn't include key, was ignored."

			else:
				used["base"] = used.get("base", 0) + 1

		presetList = [i[0:random.randrange(0,len(i.replace(".vital", "")))] for i in objKeys + [file.baseName(baseParent)]]
		presetName = ""
		for i in presetList:
			presetName += presetList[random.randrange(0,len(presetList))]

		usedSum = sum([used[i] for i in used])
		for i in used:
			used[i] = round((used[i]/usedSum)*100, 3)
			description += str(used[i]) + "% " + i + "\n"

		descriptions.append(description)
		base['comments'] = description

		filePath = file.joinPath(path, presetName[0:30].replace("-","_").replace("!","_") + ".vital")
		while file.exists(filePath):
			filePath = "_" + filePath

		names.append(filePath)
		file.writeJson(filePath, base)

	retStr = ""
	for i in range(len(names)):
		retStr += "Wrote " + names[i] + " with composition: \n" + "\t" + descriptions[i] + "\n"

	return retStr + "Errors:\t" + errors + "\nWrote presets to: \n" + filePath