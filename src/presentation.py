from os import listdir, path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt


def create_pptx_from_images(dir):
    prs = Presentation()

    layout = prs.slide_layouts[5]
    fill = layout.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0, 34, 102)

    for file_name in sorted(listdir(dir)):
        slide = prs.slides.add_slide(layout)

        title = slide.shapes.title.text_frame.paragraphs[0].add_run()
        title.font.size = Pt(28)
        title.font.bold = True
        title.font.color.rgb = RGBColor(25, 102, 255)
        
        title.text = path.splitext(file_name)[0][4:]
        pic = slide.shapes.add_picture(path.join(dir, file_name), Inches(0), Inches(1.5), width=prs.slide_width)
    

    prs.save('test.pptx')