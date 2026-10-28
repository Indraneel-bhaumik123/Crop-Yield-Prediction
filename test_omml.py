import docx
from docx.oxml import parse_xml

doc = docx.Document()
p = doc.add_paragraph('Here is an editable Word math equation:')

omml = '''<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:oMath>
    <m:r><m:t>y=ax+b</m:t></m:r>
  </m:oMath>
</m:oMathPara>'''

element = parse_xml(omml)
p._p.append(element)
doc.save('test_eq.docx')
print('Successfully saved test_eq.docx')
