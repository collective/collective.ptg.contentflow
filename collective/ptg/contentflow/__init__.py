from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.plonetruegallery import PTGMessageFactory as _
from collective.plonetruegallery.browser.views.display import BaseDisplayType
from collective.plonetruegallery.interfaces import IBaseSettings
from zope import schema


class IContentFlowSettings(IBaseSettings):
    flow_addons = schema.Tuple(
        title=_(u"label_contentflow_addons", default="Addons"),
        missing_value=None,
        default=("white",),
        required=False,
        value_type=schema.Choice(
            vocabulary=SimpleVocabulary([
                SimpleTerm("white", "white",
                    _(u"label_content_flow_addon_white", default=u"White")),
                SimpleTerm("black", "black",
                    _(u"label_content_flow_addon_black", default=u"Black")),
                SimpleTerm("gallery", "gallery",
                    _(u"label_content_flow_addon_gallery",
                        default=u"Gallery")),
                SimpleTerm("roundabout", "roundabout",
                    _(u"label_content_flow_addon_roundabout",
                        default=u"Roundabout")),
                SimpleTerm("screwdriver", "screwdriver",
                    _(u"label_content_flow_addon_screwdriver",
                        default=u"Screwdriver")),
                SimpleTerm("slideshow", "slideshow",
                    _(u"label_content_flow_addon_slideshow",
                        default=u"Slideshow"))
            ])))
    flow_max_image_height = schema.Int(
        title=_(u"label_contentflow_image_height",
            default="Max Image Height"),
        description=_(u"desc_contentflow_image_height",
            default=u"Customize how large the image shows. If zero, "
                    u"a best guess height will be selected based on the"
                    u"width. This is translated to pixels."),
        default=0,
        required=True)


class ContentFlowDisplayType(BaseDisplayType):
    name = u"contentflow"
    schema = IContentFlowSettings
    description = _(u"label_contentflow_display_type",
        default=u"Content Flow")
    typeStaticFilesRelative = '++resource++ptg.contentflow'

    def javascript(self):
        addons = self.settings.flow_addons
        if addons:
            addons = ' '.join(addons)
        else:
            addons = ''
        return """
<script type="text/javascript" charset="utf-8"
    src="%(static)s/contentflow.js" load="%(addons)s"></script>
<script>
    var flow = new ContentFlow('ContentFlow', {
        maxItemHeight: %(max_height)i,
        scaleFactorLandscape: 'max',
        /* make all events subscribable outside of here */
        onMakeInactive: function(item){
            jQuery(item.element).trigger('onMakeInactive', item);
        },
        onMakeActive: function(item){
            jQuery(item.element).trigger('onMakeActive', item);
        },
        onMoveTo: function(item){
            jQuery(item.element).trigger('onMoveTo', item);
        },
        onReachTarget: function(item){
            jQuery(item.element).trigger('onReachTarget', item);
        },
        onDrawItem: function(item){
            jQuery(item.element).trigger('onDrawItem', item);
        }
    });
</script>
""" % {
        'static': self.typeStaticFiles,
        'addons': addons,
        'max_height': self.settings.flow_max_image_height
    }
ContentFlowSettings = createSettingsFactory(ContentFlowDisplayType.schema)
