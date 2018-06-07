def add_quotes():
	new_f = open('cves.out', 'a')
	with open('cves.out.tmp', 'r') as f:
		for line in f:
			line = line[:-1]
			new_line = '"' + '","'.join(line.split(",")) + '"\n'
			new_f.write(new_line)
	new_f.close()


def main():
	with open('cves.out.tmp', 'r') as f:
		first_line = f.readline()
		if first_line.count('"') < 10:
			add_quotes()


if __name__ == "__main__":
	main()
