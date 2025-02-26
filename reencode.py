import os
import subprocess

input_directory = "D:/Vid"
output_directory = "D:/Vid/Processed"

def list_files_and_create_dirs(input_dir, output_dir):
	# Ensure the output directory exists
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	# Iterate through the files in the input directory
	for filename in os.listdir(input_dir):
		# Construct the full file path
		file_path = os.path.join(input_dir, filename)
		#
		# Check if it's a file (not a directory)
		if os.path.isfile(file_path):
			# Extract just the filename without extension
			ext = os.path.splitext(filename)[1]
			if ext != ".mp4":
				continue
			output_path = os.path.join(output_dir, filename)
			if os.path.exists(output_path): 
				print("Already processed", filename)
				continue
			result = subprocess.run(["C:\\Program Files\\ffmpeg-7.0-full_build\\bin\\ffmpeg.exe",
				"-i",file_path,
				"-map", "0",
				"-c:v","libx264",
				"-crf","30",
				#"-to","0:1:0",
				output_path],
				capture_output=True)
			print("Reencoded ", filename, ", return code: ", result.returncode)
			if result.returncode != 0:
				with open(output_path + ".output.txt", 'w') as file:
					file.write(str(result))


list_files_and_create_dirs(input_directory, output_directory)
