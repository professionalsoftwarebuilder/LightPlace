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
            layerW: 100, // Masker breedte
            layerH: 100, // 遮罩高度
            layerOpacity: 0.2, // 遮罩透明度
            layerBgc: '#000', // 遮罩背景颜色
            showPanelW: 300, // Breed weergavegebied
            showPanelH: 300, // 显示放大区域高
            marginL: 5, // 放大区域离缩略图右侧距离
            marginT: 0 // 放大区域离缩略图上侧距离
        };

        paras = $.extend({}, defaultParas, paras);

        $(this).each(function() {
            var self = $(this).css({position: 'relative'});
            var selfOffset = self.offset();
            
            /**
             * Zijn overbodig geworden
             * 
            var imageW = self.width(); // Hoogte foto
            var imageH = self.height();
            
            Weet niet waar dit ooit voor heeft gedient
            self.find('img').css({
                width: '100%',
                height: '100%'
            });
            */
            
            self.name = 'pietjepuk'
            self.attr('id', 'pietjepuk');
            //alert(self.name)
            // Brede vergroting (5x)
            var wTimes = paras.showPanelW / paras.layerW;
            // 高放大倍数
            var hTimes = paras.showPanelH / paras.layerH;

            // Vergroot de afbeelding
            var img = $('<img>').attr('src', self.attr("href")).css({
                position: 'absolute',
                left: '0',
                top: '0',
                width: self.width() * wTimes,
                height: self.height() * hTimes
            }).attr('id', 'big-img');

            // Masker (vierkant dat over de afbeelbeelding beweegt)
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

            // Zoom in gebied (de vergrote)
            var showPanel = $('<div>').css({
                display: 'none',
                position: 'absolute',
                overflow: 'hidden',
                left: self.width() + paras.marginL,
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
                }else if(x >= self.width() - paras.layerW / 2) {
                    x = self.width() - paras.layerW;
                }else {
                    x = x - paras.layerW / 2;
                }

                if(y < paras.layerH / 2) {
                    y = 0;
                } else if(y >= self.height() - paras.layerH / 2) {
                    y = self.height() - paras.layerH;
                } else {
                    y = y - paras.layerH / 2;
                }

                /// Vierkant volgt de muis
                layer.css({
                    left: x,
                    top: y
                });

                /// img (vergrote img schuift door showpanel)
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
