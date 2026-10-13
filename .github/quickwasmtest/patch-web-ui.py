from pathlib import Path
import sys

root = Path(sys.argv[1])

def patch(relative, before, after):
    path = root / relative
    text = path.read_text(encoding="utf-8")
    if text.count(before) != 1:
        raise SystemExit(f"PdfCraft patch anchor missing or ambiguous: {relative}")
    path.write_text(text.replace(before, after, 1), encoding="utf-8")

patch("crates/ui-egui/src/chrome.rs",
      'let controls_width = ui.fonts_mut(|f| f.layout_no_wrap("Discord".into(), theme::medium(13.0), t.text).size().x) + 2.0 * button + 50.0;',
      'let discord_width = if cfg!(target_arch = "wasm32") { 0.0 } else { ui.fonts_mut(|f| f.layout_no_wrap("Discord".into(), theme::medium(13.0), t.text).size().x) + 50.0 };\n                let controls_width = discord_width + 2.0 * button;')
patch("crates/ui-egui/src/chrome.rs",
      'if widgets::ghost_button_sized(ui, "messages-square", "Discord", tab_h).on_hover_text(pdfcraft_engine::links::DISCORD).clicked() {\n                        app.execute("help.discord");\n                    }',
      '#[cfg(not(target_arch = "wasm32"))]\n                    if widgets::ghost_button_sized(ui, "messages-square", "Discord", tab_h)\n                        .on_hover_text(pdfcraft_engine::links::DISCORD)\n                        .clicked()\n                    {\n                        app.execute("help.discord");\n                    }')
patch("crates/ui-egui/src/widgets.rs",
      '        for (i, l) in pdfcraft_engine::links::LINKS.iter().enumerate() {\n            let resp = if i == 0 { icon_pill(ui, l.icon, tl!("Join our Discord"), true) } else { icon_pill(ui, l.icon, tl!(l.label), false) };',
      '        for (i, l) in pdfcraft_engine::links::LINKS.iter().enumerate() {\n            if cfg!(target_arch = "wasm32") && i == 0 { continue; }\n            let resp = if i == 0 { icon_pill(ui, l.icon, tl!("Join our Discord"), true) } else { icon_pill(ui, l.icon, tl!(l.label), false) };')
patch("crates/ui-egui/src/home.rs",
      'ui.label(egui::RichText::new(tl!("Get help, share feedback and follow development on Discord.")).color(t.text_muted));',
      '#[cfg(not(target_arch = "wasm32"))]\n                            ui.label(egui::RichText::new(tl!("Get help, share feedback and follow development on Discord.")).color(t.text_muted));')
