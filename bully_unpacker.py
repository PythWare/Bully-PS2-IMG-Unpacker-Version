import os
import sys

dir_extension = ".DIR" # File extension for DIR metadata files
img_extension = ".IMG" # IMG extension for IMG containers
folder = "_UNPACKED" # folder to store unpacked files
error_file = "Unpacker_Error.txt" # file to store possible errors

def Unpacker():
    """This function handles the file logic"""
    total_files = 0 # total files unpacked
    packed_filename = None # used for filenames packed within the DIR files
    packed_base_file_size = None # used for file sizes stored within the DIR files
    packed_file_data = None # used for file data packed within the IMG files
    shifted_file_size = None # used to obtain the actual file size which is bit shifting to the left 11 times
    
    if len(sys.argv) > 1:
        dir_file = sys.argv[1] # get the dropped file
        if dir_extension in dir_file: # if the extension .DIR is within the dropped file's name
            file_basename = os.path.basename(dir_file).split('.')[0] # extract the extension from the filename
            extraction_folder = file_basename + folder # get the file's basename and add _UNPACKED as part of the folder name
            os.makedirs(extraction_folder, exist_ok = True) # create the folder for file extraction if it doesn't exist
            img_file = file_basename + img_extension # combine the filename with the IMG extension
            if os.path.isfile(img_file): # check if the IMG file exists
                with open(dir_file, "rb") as dir_file, open(img_file, "rb") as img_file: # open the DIR and IMG files for reading
                    while True: # read until the end of the file
                        offset = dir_file.read(4) # read offset(will not be used for file seeking so integer conversion is not needed)
                        if not offset: # if at the end of the file
                            break
                        packed_base_file_size = int.from_bytes(dir_file.read(4), "little") # get the base file size
                        shifted_file_size = packed_base_file_size << 11 # bit shift to get the file's actual size
                        packed_filename = dir_file.read(24).decode().strip('\x00') # get, decode, and remove the null values to obtain filenames
                        total_files += 1 # icnrement by 1 for each file unpacked
                        print(f" File number {total_files}'s file {packed_filename}") # print the file number and the file's name
                        packed_file_data = img_file.read(shifted_file_size) # read file data equal to the size of the bit shifted file size
                        file_unpack_handling(extraction_folder, packed_filename, packed_file_data) # call the file unpacking function and pass the data needed
                            
            else: # if the dropped file does not have a matching .IMG file
                log_error(f"Error: The file {dir_file} does not seem to have a matching {img_extension} file, this script requires it to exist.", func_name="Unpacker")
                sys.exit()
        else: # if the file is not a .DIR file
            log_error(f"Error: The file '{dir_file}' is not a .DIR file, please only use the script with .DIR files.", func_name="Unpacker")
            sys.exit()
            
    else: # if the dropped file is not a DIR file
        log_error(f"Error: Either a file was not dropped onto the script or the command prompt did not receive a filename as part of the command.", func_name="Unpacker")
        sys.exit()
    return total_files
def file_unpack_handling(path: str, file: str, file_data: int):
    """This function handles the file creation of the packed files"""
    try:
        with open(os.path.join(path, file), "wb") as dir_file: # create the packed file
            dir_file.write(file_data) # write the file data
    except PermissionError:
        log_error(f"Permission denied for file {packed_filename}.", func_name="file_unpacker_handling")
        sys.exit()
    except IOError as e:
        log_error(f"An I/O error occured. Details: {e}", func_name="file_unpack_handling")
        sys.exit()
    except Exception as e:
        log_error(f"Failed to create or write to {os.path.join(folder, file)}.", func_name="file_unpack_handling", error=str(e))
        sys.exit()
    else:
        remove_error_file() # remove the error file if it exists since an error did not occur

#file_check_protocol(dir_file: str, img_file: str) -> None:
def remove_error_file() -> None:
        """This is a cleanup function that will remove the error file when no error is detected"""
        if os.path.isfile(error_file): # if the error file exists
            os.remove(error_file) # remove the error file
            
def log_error(message: str, func_name: str = None, **kwargs) -> None:
        """This function handles error detection"""

        try:
            with open(error_file, "a") as w1:  # open error file
                if func_name:
                    w1.write(f"Error in function {func_name}: \n{message}\n")  # Log function name
                else:
                    w1.write(f"Error: {message}\n")  # Log just the message

                if kwargs:
                    for key, value in kwargs.items():
                        w1.write(f"{key}: \n{value}\n")  # Log additional context
        except Exception as e:
            print(f"Failed to write to error log: {e}")
            
if __name__ == "__main__":
    total_files = Unpacker()
    input(f"Task finished, {total_files} files were unpacked. You may exit now.") # used for user to see results and to keep script open
