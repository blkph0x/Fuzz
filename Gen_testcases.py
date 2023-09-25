import os
import random
import string

def random_string(length):
    """Generate a random string of a given length."""
    return ''.join(random.choice(string.printable) for _ in range(length))

def generate_random_pdf(filename, num_pages=5, num_objects_per_page=10, max_offset=1000):
    """Generate a random PDF file with various structures and potentially problematic inputs."""
    with open(os.path.join('testcases', filename), 'wb') as f:  # Save in the 'testcases' folder
        # PDF header
        f.write(b'%PDF-1.7\n')

        # PDF catalog
        f.write(b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n')

        # PDF page tree
        f.write(b'2 0 obj\n<< /Type /Pages /Kids [')
        for page_num in range(num_pages):
            page_obj_num = num_pages * 2 + 3 + page_num * (num_objects_per_page + 4)
            f.write(f'{page_obj_num} 0 R '.encode('utf-8'))
        f.write(b'] /Count ' + str(num_pages).encode('utf-8') + b' >>\nendobj\n')

        # Generate random objects per page
        for page_num in range(num_pages):
            page_obj_num = num_pages * 2 + 3 + page_num * (num_objects_per_page + 4)
            
            # Page content stream
            content_stream = (f'{page_obj_num} 0 obj\n<< /Length 6 0 R >>\nstream\nq\nBT\n/F1 12 Tf\n10 10 Td\n('
                              + random_string(10) + ') Tj\nET\nQ\nendstream\nendobj\n').encode('utf-8')
            f.write(content_stream)
            
            # Generate other objects on the page (annotations, fonts, images, forms, etc.)
            for _ in range(num_objects_per_page):
                object_number = page_obj_num + _ + 1
                generation_number = 0

                # Randomly select object type (dictionary, stream, annotation, image, form)
                obj_type = random.choice(["dict", "stream", "annotation", "image", "form"])
                if obj_type == "dict":
                    # Generate a dictionary object with variations
                    dictionary_content = random_string(random.randint(10, 50))
                    font_variation = f'/F{_ % 2 + 1}'  # Use two fonts alternately
                    obj_content = (f'{object_number} {generation_number} obj\n<< {font_variation} /Size {_} '
                                   + dictionary_content + ' >>\nendobj\n').encode('utf-8')
                    f.write(obj_content)
                elif obj_type == "stream":
                    # Generate a stream object with variations
                    stream_content = os.urandom(random.randint(10, max_offset))
                    obj_content = (f'{object_number} {generation_number} obj\n<< >>\nstream\n'.encode('utf-8')
                                   + stream_content + b'\nendstream\nendobj\n')
                    f.write(obj_content)
                elif obj_type == "annotation":
                    # Generate annotation objects with JavaScript actions
                    annotation_content = random_string(random.randint(10, 50))
                    js_action = f'/JS <{random_string(20)}>'
                    obj_content = (f'{object_number} {generation_number} obj\n<< /Type /Annot /Subtype /Text /Contents ({annotation_content}) {js_action} >>\nendobj\n')
                    f.write(obj_content.encode('utf-8'))
                elif obj_type == "image":
                    # Generate image objects (as a placeholder)
                    image_data = os.urandom(10000)
                    obj_content = (f'{object_number} {generation_number} obj\n<< /Type /XObject /Subtype /Image /Width 100 /Height 100 /BitsPerComponent 8 /ColorSpace /DeviceRGB /Length {len(image_data)} >>\nstream\n').encode('utf-8')
                    f.write(obj_content)
                    f.write(image_data)
                    f.write(b'\nendstream\nendobj\n')
                elif obj_type == "form":
                    # Generate interactive form elements (text fields)
                    form_field_name = random_string(random.randint(5, 20))
                    obj_content = (f'{object_number} {generation_number} obj\n<< /Type /Annot /Subtype /Widget /FT /Tx /T ({form_field_name}) /F {_ % 2 + 1} 0 R /AP 5 0 R >>\nendobj\n')
                    f.write(obj_content.encode('utf-8'))

        # PDF font objects with variations
        f.write(b'3 0 obj\n<< /Type /Font /Subtype /Type1 /Name /F1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding /ItalicAngle 0 >>\nendobj\n')
        f.write(b'4 0 obj\n<< /Type /Font /Subtype /Type1 /Name /F2 /BaseFont /Times-Roman /Encoding /WinAnsiEncoding /ItalicAngle 0 >>\nendobj\n')

        # PDF image XObject (placeholder)
        image_data = os.urandom(10000)
        f.write((f'5 0 obj\n<< /Type /XObject /Subtype /Image /Width 100 /Height 100 /BitsPerComponent 8 /ColorSpace /DeviceRGB /Length {len(image_data)} >>\nstream\n').encode('utf-8'))
        f.write(image_data)
        f.write(b'\nendstream\nendobj\n')

        # PDF trailer
        f.write(b'xref\n0 6\n0000000000 65535 f \n0000000010 00000 n \n0000000123 00000 n \n0000000345 00000 n \n0000000456 00000 n \n0000000567 00000 n \ntrailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n500\n%%EOF\n')

if __name__ == "__main__":
    num_test_cases = 5000  # Number of test cases to generate
    os.makedirs('testcases', exist_ok=True)  # Create the 'testcases' folder if it doesn't exist

    for i in range(num_test_cases):
        pdf_filename = f"test_case_{i}.pdf"
        generate_random_pdf(pdf_filename)
        print(f"Generated {pdf_filename}")
