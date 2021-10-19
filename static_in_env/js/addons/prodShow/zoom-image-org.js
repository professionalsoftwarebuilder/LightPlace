//alert('begin zoom-image');

;(function($) {
    /**
     * 1, De grootte van de miniatuur is hetzelfde als de grootte van de bovenliggende container
     * 2, Bovenliggende container href Het kenmerk is het HD-beeldpad
     */
    $.fn.zoomImage = function(paras) {
        /**
         * Standaardparameter
         */
        var defaultParas = {
            layerW: 100, // 遮罩宽度
            layerH: 100, // 遮罩高度
            layerOpacity: 0.2, // 遮罩透明度
            layerBgc: '#000', // 遮罩背景颜色
            showPanelW: 500, // 显示放大区域宽
            showPanelH: 500, // 显示放大区域高
            marginL: 5, // 放大区域离缩略图右侧距离
            marginT: 0 // 放大区域离缩略图上侧距离
        };

        paras = $.extend({}, defaultParas, paras);

        $(this).each(function() {
            var self = $(this).css({position: 'relative'});
            var selfOffset = self.offset();
            var imageW = self.width(); // Hoogte foto
            var imageH = self.height();

            self.find('img').css({
                width: '100%',
                height: '100%'
            });

            // Brede vergroting
            var wTimes = paras.showPanelW / paras.layerW;
            // 高放大倍数
            var hTimes = paras.showPanelH / paras.layerH;

            // Vergroot de afbeelding
            var img = $('<img>').attr('src', self.attr("href")).css({
                position: 'absolute',
                left: '0',
                top: '0',
                width: imageW * wTimes,
                height: imageH * hTimes
            }).attr('id', 'big-img');

            // Masker
            var layer = $('<div>').css({
                display: 'none',
                position: 'absolute',
                left: '0',
                top: '0',
                backgroundColor: paras.layerBgc,
                width: paras.layerW,
                height: paras.layerH,
                opacity: paras.layerOpacity,
                border: '1px solid #ccc',
                cursor: 'crosshair'
            });

            // Zoom in gebied
            var showPanel = $('<div>').css({
                display: 'none',
                position: 'absolute',
                overflow: 'hidden',
                left: imageW + paras.marginL,
                top: paras.marginT,
                width: paras.showPanelW,
                height: paras.showPanelH
            }).append(img);

            self.append(layer).append(showPanel);

            self.on('mousemove', function(e) {
                // De coördinaten van de muis ten opzichte van de miniatuurcontainer
                var x = e.pageX - selfOffset.left;
                var y = e.pageY - selfOffset.top;

                if(x <= paras.layerW / 2) {
                    x = 0;
                }else if(x >= imageW - paras.layerW / 2) {
                    x = imageW - paras.layerW;
                }else {
                    x = x - paras.layerW / 2;
                }

                if(y < paras.layerH / 2) {
                    y = 0;
                } else if(y >= imageH - paras.layerH / 2) {
                    y = imageH - paras.layerH;
                } else {
                    y = y - paras.layerH / 2;
                }

                layer.css({
                    left: x,
                    top: y
                });

                img.css({
                    left: -x * wTimes,
                    top: -y * hTimes
                });
            }).on('mouseenter', function() {
                layer.show();
                showPanel.show();
            }).on('mouseleave', function() {
                layer.hide();
                showPanel.hide();
            });
        });
    }
})(jQuery);

//alert('eind zoom image');
