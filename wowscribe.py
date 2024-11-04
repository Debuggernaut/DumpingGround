
import mlx_whisper
import os
import subprocess

input_directory = "/Volumes/Vid/"
output_directory = "/Volumes/MacBak/RawAudio"

def transcribe_audio_streams(vidname, input_file, audio_output_path, skip_extraction=0):
	for stream_index in range(3):  # Loop for streams 0 to 2
		audio_path = os.path.join(audio_output_path, f"{vidname}_audio_{stream_index}.aac")
		if skip_extraction == 0:
			result = subprocess.run(["ffmpeg",
				"-i",input_file,
				"-map", f"0:a:{stream_index}",
				"-c","copy",
				audio_path],
				capture_output=True)

		if skip_extraction != 0 or result.returncode == 0:
			print("Beginning transcription of " + audio_path)
			text_path = os.path.join(audio_output_path, f"{vidname}_text_{stream_index}")
			if os.path.exists(audio_path) and not os.path.exists(text_path):
				text = mlx_whisper.transcribe(audio_path, 
					path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
					initial_prompt="This is a person playing World of Warcraft, an online game, with friends",
					verbose=False) ["text"]
				with open(text_path, 'w') as file:
					file.write(text)

#killswitch = 5

def list_files_and_create_dirs(input_dir, output_dir):
	#global killswitch
	"""
	Lists all files in the input directory and creates new directories in the output directory
	with names based on the filenames from the input directory.

	:param input_dir: Path to the directory containing the files.
	:param output_dir: Path where new directories will be created.
	"""
	
	# Ensure the output directory exists
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	# Iterate through the files in the input directory
	for filename in os.listdir(input_dir):
		# Construct the full file path
		file_path = os.path.join(input_dir, filename)
		
		# Check if it's a file (not a directory)
		if os.path.isfile(file_path):
			# Extract just the filename without extension
			dir_name = os.path.splitext(filename)[0]
			
			# Construct the new directory path
			new_dir_path = os.path.join(output_dir, dir_name)
			
			# Create the new directory
			skip_extraction=0
			try:
				os.makedirs(new_dir_path)  # This will create the directory if it doesn't exist
				print(f"Created directory: {new_dir_path}")
			except FileExistsError:
				print(f"Directory already exists: {new_dir_path}")
				skip_extraction=1
			transcribe_audio_streams(dir_name, file_path, new_dir_path, skip_extraction)
				#killswitch = killswitch - 1
				#if killswitch == 0:
				#	print("KILL LIMIT HIT")
				#	return


list_files_and_create_dirs(input_directory, output_directory)
