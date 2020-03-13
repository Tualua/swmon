from flask import Blueprint, render_template, redirect, url_for
from ..models import db, Router
from ..forms import EditRouterForm

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/', methods=['GET', 'POST'])
def settings():
    router = Router.get_router()
    formRouter = EditRouterForm(obj=router)
    if formRouter.validate_on_submit() and formRouter.submitRouter.data:
        if router:
            router.ipaddress, router.port = formRouter.ipaddress.data, formRouter.port.data
            db.session.commit()
            return redirect(url_for('settings.settings'))
        else:
            router = Router(ipaddress=formRouter.ipaddress.data, port=formRouter.port.data)
            db.session.add(router)
            db.session.commit()
            return redirect(url_for('settings.settings'))
    return render_template('settings.html', formRouter=formRouter)
