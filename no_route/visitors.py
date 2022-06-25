from typing import List, Optional, cast

import libcst as cst
import libcst.matchers as m
from libcst.codemod import VisitorBasedCodemodCommand


class RouteDecoratorVisitor(m.MatcherDecoratableVisitor):
    @m.call_if_inside(
        m.Decorator(
            m.Call(
                m.Attribute(attr=m.Name("route")),
                args=[m.ZeroOrMore(), m.Arg(keyword=m.Name("methods")), m.ZeroOrMore()],
            )
        )
    )
    @m.visit(m.Arg(keyword=m.Name("methods")))
    def _visit_route(self, node: cst.Arg) -> None:
        elements = cst.ensure_type(node.value, cst.List).elements
        if len(elements) > 1:
            print("Create functions for the different HTTP methods.")
        else:
            print("Use the new style to write endpoint functions.")


class RouteDecoratorCommand(VisitorBasedCodemodCommand):
    @m.leave(
        m.Decorator(
            m.Call(
                m.Attribute(attr=m.Name("route")),
                args=[
                    m.ZeroOrMore(),
                    m.Arg(
                        keyword=m.Name("methods"),
                        value=m.List(elements=[m.AtMostN(n=1)]),
                    ),
                    m.ZeroOrMore(),
                ],
            )
        )
    )
    def _leave_route(
        self, original_node: cst.Decorator, updated_node: cst.Decorator
    ) -> cst.Decorator:
        decorator = cst.ensure_type(updated_node.decorator, cst.Call)
        args_to_keep: List[cst.Arg] = []
        method: Optional[str] = None
        for arg in decorator.args:
            if m.matches(arg, m.Arg(keyword=m.Name("methods"))):
                elements = cst.ensure_type(arg.value, cst.List).elements
                element = cst.ensure_type(elements[0], cst.Element)
                method = cst.ensure_type(element.value, cst.SimpleString).value
                method = method.strip('"').lower()
            else:
                args_to_keep.append(arg.with_changes(comma=cst.MaybeSentinel.DEFAULT))
        method = cast(str, method)
        return updated_node.with_changes(
            decorator=decorator.with_changes(
                func=decorator.func.with_changes(attr=cst.Name(value=method)),
                args=args_to_keep,
            )
        )
