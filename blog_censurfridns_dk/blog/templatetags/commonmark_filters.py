from django import template
import CommonMark

register = template.Library()

@register.filter(is_safe=True)
def markdown(input):
    parser = CommonMark.Parser()
    renderer = CommonMark.HtmlRenderer()
    ast = parser.parse(input)
    return renderer.render(ast)

