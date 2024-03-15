from magic_pdf.libs.commons import s3_image_save_path, join_path
from magic_pdf.libs.markdown_utils import ocr_escape_special_markdown_char
from magic_pdf.libs.ocr_content_type import ContentType


def ocr_mk_nlp_markdown(pdf_info_dict: dict):
    markdown = []

    for _, page_info in pdf_info_dict.items():
        blocks = page_info.get("preproc_blocks")
        if not blocks:
            continue
        for block in blocks:
            for line in block['lines']:
                line_text = ''
                for span in line['spans']:
                    if not span.get('content'):
                        continue
                    content = ocr_escape_special_markdown_char(span['content'])  # 转义特殊符号
                    if span['type'] == ContentType.InlineEquation:
                        content = f"${content}$"
                    elif span['type'] == ContentType.InterlineEquation:
                        content = f"$$\n{content}\n$$"
                    line_text += content + ' '
                # 在行末添加两个空格以强制换行
                markdown.append(line_text.strip() + '  ')
    return '\n'.join(markdown)


def ocr_mk_mm_markdown(pdf_info_dict: dict):

    markdown = []

    for _, page_info in pdf_info_dict.items():
        blocks = page_info.get("preproc_blocks")
        if not blocks:
            continue
        for block in blocks:
            for line in block['lines']:
                line_text = ''
                for span in line['spans']:
                    if not span.get('content'):
                        if not span.get('image_path'):
                            continue
                        else:
                            content = f"![]({join_path(s3_image_save_path, span['image_path'])})"
                    else:
                        content = ocr_escape_special_markdown_char(span['content'])  # 转义特殊符号
                        if span['type'] == ContentType.InlineEquation:
                            content = f"${content}$"
                        elif span['type'] == ContentType.InterlineEquation:
                            content = f"$$\n{content}\n$$"
                    line_text += content + ' '
                # 在行末添加两个空格以强制换行
                markdown.append(line_text.strip() + '  ')
    return '\n'.join(markdown)


def mk_mm_markdown2(pdf_info_dict:dict):
    markdown = []
    for _, page_info in pdf_info_dict.items():
        paras = page_info.get("para_blocks")
        if not paras:
            continue
        for para in paras:
            para_text = ''
            for line in para:
                for span in line['spans']:
                    span_type = span.get('type')
                    if span_type == ContentType.Text:
                        para_text += span['content']
                    elif span_type == ContentType.InlineEquation:
                        para_text += f" ${span['content']}$ "
                    elif span_type == ContentType.InterlineEquation:
                        para_text += f"$$\n{span['content']}\n$$ "
                    elif span_type == ContentType.Image:
                        para_text += f"![]({join_path(s3_image_save_path, span['image_path'])})"
            markdown.append(para_text)

    return '\n\n'.join(markdown)


def ocr_mk_mm_standard_format():
    '''
    content_list
    type string image/text/table/equation(行间的单独拿出来，行内的和text合并)

    '''
    pass