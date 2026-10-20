// Chay 14 kich ban UAT (05-test/S17-uat.md) tren prototype. In Dat/Khong dat tung kich ban.
// Chay: npm i playwright && npx playwright install chromium && node 05-test/automation/uat_prototype.js [URL]
const { chromium } = require('playwright');
const URL = process.argv[2] || 'https://taint7684.github.io/eudr-coffee-ba/prototype/';
const res = [];
const ok = (id, cond, note) => { res.push([id, cond ? 'ĐẠT' : 'KHÔNG ĐẠT', note]); };
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 }, acceptDownloads: true });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  let promptText = 'Thiếu đa giác lô LO-00002';
  p.on('dialog', d => d.accept(promptText));
  await p.goto(URL); await p.waitForTimeout(1500);
  const role = async r => { await p.selectOption('#role', r); await p.waitForTimeout(400); };
  const go = async k => { await p.evaluate(k => go(k), k); await p.waitForTimeout(700); };
  const txt = async s => (await p.textContent(s).catch(() => '')) || '';
  const close = async () => p.evaluate(() => closeModal());

  // UAT-01
  await role('Đại lý'); await go('SCR01');
  await p.click('#addF'); await p.fill('#fn', 'Nguyễn Văn Test'); await p.fill('#fp', '0912345678');
  await p.selectOption('#fc', { index: 1 }); await p.click('#fs');
  const e1 = await txt('#ferr'); await p.check('#fok'); await p.click('#fs'); await p.waitForTimeout(300);
  const m1 = await txt('#modalBody'); await close();
  ok('UAT-01', e1.includes('đồng ý') && m1.includes('Đã tạo'), 'chặn khi chưa đồng ý; tạo được khi đồng ý');

  // UAT-02
  await go('SCR02'); await p.fill('#pa', '1.20'); await p.dispatchEvent('#pa', 'input');
  await p.click('#mPt'); await p.fill('#dn', 'CS123456'); await p.click('#ps'); await p.waitForTimeout(300);
  const m2 = await txt('#modalBody'); const geo2 = m2.includes('Đã lưu'); await close();
  ok('UAT-02', geo2, 'Lấy điểm GPS đặt điểm ngay, lưu được');

  // UAT-03
  await go('SCR02'); await p.fill('#pa', '4.01'); await p.dispatchEvent('#pa', 'input'); await p.waitForTimeout(200);
  const ptDisabled = await p.isDisabled('#mPt');
  await p.click('#mPg');
  const box = await (await p.$('#pmap')).boundingBox(); const cx = box.x + box.width * 0.75, cy = box.y + box.height * 0.75;
  for (const [dx, dy] of [[-90, -90], [90, -90], [90, 90], [-90, 90]]) await p.mouse.click(cx + dx, cy + dy);
  await p.fill('#dn', 'CS654321'); await p.click('#ps'); await p.waitForTimeout(300);
  let e3 = await txt('#perr');
  if (e3.includes('BR-004')) { await p.selectOption('#why', { index: 1 }); await p.click('#ps'); await p.waitForTimeout(300); }
  if ((await txt('#perr')).includes('BR-005')) e3 += ' [trùng lô có sẵn]';
  const m3 = await txt('#modalBody'); await close();
  ok('UAT-03', ptDisabled && m3.includes('Đã lưu'), `nút điểm khóa=${ptDisabled}; ${e3.includes('BR-004') ? 'có cảnh báo lệch diện tích → chọn lý do → lưu' : 'lưu'}`);

  // UAT-04
  await go('SCR02'); await p.fill('#pa', '1.0'); await p.dispatchEvent('#pa', 'input'); await p.click('#mPg');
  const b4 = await (await p.$('#pmap')).boundingBox(); const x4 = b4.x + b4.width * 0.25, y4 = b4.y + b4.height * 0.75;
  for (const [dx, dy] of [[-60, -60], [60, 60], [60, -60], [-60, 60]]) await p.mouse.click(x4 + dx, y4 + dy);
  await p.fill('#dn', 'CS111111'); await p.click('#ps'); await p.waitForTimeout(300);
  const e4 = await txt('#perr');
  ok('UAT-04', e4.includes('tự cắt'), 'đa giác hình số 8 bị chặn');

  // UAT-05, 06, 07
  await role('Tuân thủ'); await go('SCR03');
  const det = await txt('#det'); const q = await txt('main');
  ok('UAT-05', det.includes('Quy tắc') && det.includes('Phiên bản dữ liệu'), 'chi tiết lô có quy tắc, % giao rừng, phiên bản dữ liệu');
  ok('UAT-06', q.includes('Quá hạn') && q.includes('SLA 14 ngày'), 'hàng đợi có SLA và dòng quá hạn');
  await p.selectOption('#vx', 'Đạt'); await p.click('#vs'); await p.waitForTimeout(200);
  const e7 = await txt('#verr');
  await p.setInputFiles('#ve', { name: 'anh-2019.jpg', mimeType: 'image/jpeg', buffer: Buffer.from('x') });
  await p.fill('#vd', '2019-06-15'); await p.selectOption('#vx', 'Đạt'); await p.fill('#vr', 'Ảnh vệ tinh 2019 thể hiện vườn cà phê');
  await p.click('#vs'); await p.waitForTimeout(400);
  const after7 = await txt('#det');
  await role('Quản lý'); await go('SCR07'); const audit7 = await txt('main');
  ok('UAT-07', e7.includes('bằng chứng') && after7.includes('Đã xác minh') && audit7.includes('Quyết định Vùng xám'), 'chặn khi thiếu bằng chứng; lưu quyết định; audit ghi trước/sau');

  // UAT-08, 09
  await role('Đại lý'); await go('SCR04');
  const pick = await p.evaluate(() => {
    const mine = S.plots.filter(x => farmerOf(x).agent_id === S.agent);
    const gray = mine.find(x => x.risk_status !== 'Đạt' || x.legal_status !== 'Đủ');
    const good = mine.filter(x => x.risk_status === 'Đạt' && x.legal_status === 'Đủ').sort((a, b) => a.area_declared_ha - b.area_declared_ha)[0];
    return { gray: gray && [gray.farmer_id, gray.plot_id], good: good && [good.farmer_id, good.plot_id] };
  });
  await p.selectOption('#tf', pick.gray[0]); await p.selectOption('#tp', pick.gray[1]); await p.waitForTimeout(200);
  const euDisabled = await p.evaluate(() => document.querySelector('#ts').options[0].disabled);
  ok('UAT-08', euDisabled, `lô ${pick.gray[1]} chưa đủ điều kiện → khóa dòng EU`);
  await p.selectOption('#tf', pick.good[0]); await p.selectOption('#tp', pick.good[1]); await p.fill('#tk', '20000'); await p.selectOption('#ts', 'EU');
  await p.click('#tsave'); await p.waitForTimeout(300); const m9 = await txt('#modalBody'); await close();
  ok('UAT-09', m9.includes('Vượt sản lượng'), 'giao dịch vượt sản lượng chờ Tuân thủ xác nhận');

  // UAT-10
  await role('Thu mua'); await go('SCR05');
  const inputs = await p.$$('[data-r]'); await inputs[0].fill('99999999'); await p.click('#aSave'); await p.waitForTimeout(300);
  const e10 = await txt('#aerr');
  const inputs2 = await p.$$('[data-r]'); await inputs2[0].fill('5000'); await p.click('#aSave'); await p.waitForTimeout(400);
  const kg10 = await txt('#sd');
  ok('UAT-10', e10.includes('vượt') && kg10.includes('5.000 kg'), 'chặn phân bổ vượt; lưu phân bổ hợp lệ');

  // UAT-12 roi UAT-11
  await role('Tuân thủ'); await go('SCR05');
  const dl = p.waitForEvent('download'); await p.click('#mk'); const d = await dl;
  const gj = JSON.parse(require('fs').readFileSync(await d.path(), 'utf8'));
  const okGj = gj.properties.hs_code === '0901' && gj.properties.country_of_production === 'VN' && gj.features.length > 0 && gj.features.every(f => f.geometry.type === 'Point' || f.geometry.type === 'Polygon');
  await p.waitForTimeout(400);
  await p.click('#rej'); await p.waitForTimeout(400); const s12 = await txt('#sd');
  ok('UAT-12', s12.includes('Từ chối lần trước') && s12.includes('Nháp'), 'từ chối → về Nháp, hiện lý do');
  const dl2 = p.waitForEvent('download'); await p.click('#mk'); await dl2; await p.waitForTimeout(300);
  await p.fill('#ref', 'EU-DDS-2026-000123'); await p.click('#okR'); await p.waitForTimeout(300); const s11 = await txt('#sd');
  ok('UAT-11', okGj && s11.includes('Được chấp nhận') && s11.includes('lưu đến'), `GeoJSON ${gj.features.length} lô, HS 0901, VN; có số tham chiếu và hạn lưu 5 năm`);

  // UAT-13
  await role('Đại lý'); await go('SCR05'); const a = await txt('main');
  await role('Thu mua'); await go('SCR02'); const bb = await txt('main');
  await role('Tuân thủ'); await go('SCR07'); const dis = await p.isDisabled('[data-k="buffer_m"]');
  ok('UAT-13', a.includes('Không có quyền') && bb.includes('Không có quyền') && dis, 'phân quyền đúng ma trận');

  // UAT-14
  await role('Quản lý'); await go('SCR07'); await p.fill('[data-k="buffer_m"]', '30'); await p.click('#pSave'); await p.waitForTimeout(300);
  const a14 = await txt('main');
  ok('UAT-14', a14.includes('buffer_m') && a14.includes('Sửa'), 'đổi vùng đệm 50 → 30, audit ghi lại');

  console.table(res);
  console.log('Lỗi JavaScript:', errs.length ? errs : 'không có');
  await b.close();
})();
