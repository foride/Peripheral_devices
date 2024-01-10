import wia_scan
from PIL import Image

def scan_and_save():
    dpi = int(input("Enter resolution (300 or 600 dpi): "))
    mode = input("Enter scan mode (RGB or Grayscale): ")
    rotation = int(input("Enter rotation angle (0, 90, 180, or 270 degrees): "))
    contrast = int(input("Enter contrast value from -1000 to 1000: "))
    output_file = input("Enter output file path (or press Enter to skip saving): ").strip()


    scanner = wia_scan.prompt_choose_device_and_connect()

    
    profile = wia_scan.get_default_profile()
    profile.update({'mode': mode, 'dpi': dpi, 'contrast': contrast})
    profile['height'] = dpi * 11,69
    profile['width'] = dpi

    wia_scan.print_device_properties(scanner)

    image = wia_scan.scan_side(device=scanner, verbose=True, scan_profile=profile)

    if rotation != 0:
        image = image.rotate(rotation, expand=True)

    image.show()

    if output_file:
        image.save(output_file)

if __name__ == "__main__":
    scan_and_save()
