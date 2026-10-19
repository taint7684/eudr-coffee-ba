// T8.1 — So hai nguồn: mất cây che phủ Hansen 2021+ so với bản đồ rừng mốc 2020 của EU (JRC GFC2020).
// Chạy trong Google Earth Engine Code Editor (https://code.earthengine.google.com), tài khoản phi thương mại.
// Kết quả: CSV theo huyện → lưu về 03-data/processed/T8_1_hansen_vs_gfc2020.csv
//
// Câu hỏi: bao nhiêu % "mất cây che phủ" sau 2020 nằm trên đất mà bản đồ EU coi là RỪNG năm 2020?
// Phần còn lại = mất cây che phủ ngoài rừng (cây trồng, nông lâm kết hợp) → KHÔNG phải phá rừng theo EUDR Điều 2(3), 2(6).
//
// [Unverified] Kiểm tra mã asset trong Data Catalog trước khi chạy:
//   - Hansen: chọn phiên bản mới nhất (vd UMD/hansen/global_forest_change_2025_v1_13).
//   - GFC2020: JRC/GFC2020/V4 (V2, V3 đã deprecated).
//   - geoBoundaries: WM/geoLab/geoBoundaries/600/ADM2.

var HANSEN = 'UMD/hansen/global_forest_change_2024_v1_12';   // TODO: đổi sang bản mới nhất có năm 2025
var CANOPY = 30;          // ASM-11 — chạy lại với 10 để phân tích độ nhạy (ngưỡng rừng EUDR là 10%)
var LOSS_FROM = 21;       // lossyear 21 = năm 2021

var DISTRICTS = ['Buon Don', 'Buon Ho', 'Buon Ma Thuot', 'Cu Kuin', 'Cu Mgar', 'EA Hleo', 'Ea Kar',
                 'Ea Sup', 'Krong A Na', 'Krong Bong', 'Krong Buk', 'Krong Nang', 'Krong Pac', 'Lak',
                 'Mdrak District'];

var adm2 = ee.FeatureCollection('WM/geoLab/geoBoundaries/600/ADM2')
  .filter(ee.Filter.eq('shapeGroup', 'VNM'))
  .filter(ee.Filter.inList('shapeName', DISTRICTS));

var gfc = ee.Image(HANSEN);
var tc2000 = gfc.select('treecover2000').gte(CANOPY);
var loss21 = gfc.select('lossyear').gte(LOSS_FROM).and(tc2000);

var forest2020 = ee.ImageCollection('JRC/GFC2020/V4').mosaic().select('Map').eq(1);

var areaHa = ee.Image.pixelArea().divide(1e4);
var stack = ee.Image.cat([
  areaHa.updateMask(loss21).rename('loss21_ha'),
  areaHa.updateMask(loss21.and(forest2020)).rename('loss21_in_forest2020_ha'),
  areaHa.updateMask(forest2020).rename('forest2020_ha')
]);

var stats = stack.reduceRegions({collection: adm2, reducer: ee.Reducer.sum(), scale: 30, tileScale: 4})
  .map(function (f) {
    var a = ee.Number(f.get('loss21_ha'));
    var b = ee.Number(f.get('loss21_in_forest2020_ha'));
    return f.set('share_in_forest2020', ee.Algorithms.If(a.gt(0), b.divide(a), 0))
            .set('canopy_threshold', CANOPY).set('hansen_asset', HANSEN);
  });

print(stats.select(['shapeName', 'loss21_ha', 'loss21_in_forest2020_ha', 'share_in_forest2020', 'forest2020_ha']));

Map.centerObject(adm2, 9);
Map.addLayer(forest2020.selfMask(), {palette: ['1b7837']}, 'Rừng 2020 (JRC GFC2020)');
Map.addLayer(loss21.selfMask(), {palette: ['d6604d']}, 'Mất cây che phủ 2021+ (Hansen)');
Map.addLayer(loss21.and(forest2020).selfMask(), {palette: ['762a83']}, 'Mất trong rừng 2020');
Map.addLayer(adm2.style({color: '333333', fillColor: '00000000', width: 1}), {}, 'Huyện');

Export.table.toDrive({
  collection: stats,
  description: 'T8_1_hansen_vs_gfc2020',
  fileFormat: 'CSV',
  selectors: ['shapeName', 'loss21_ha', 'loss21_in_forest2020_ha', 'share_in_forest2020', 'forest2020_ha',
              'canopy_threshold', 'hansen_asset']
});
