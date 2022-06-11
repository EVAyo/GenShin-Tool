using DGP.Genshin.Core;
using DGP.Genshin.Core.LifeCycle;
using DGP.Genshin.Core.Plugins;
using System;
using System.Windows.Media;

[assembly: SnapGenshinPlugin]

namespace DGP.Genshin.Skin.Pink;

/// <summary>
/// ��ɫƤ�����
/// </summary>
public class PinkSkinPlugin : IPlugin, IAppStartUp
{
    /// <inheritdoc/>
    public bool IsEnabled { get => true; }

    /// <inheritdoc/>
    public string Name { get => "Pink Skin"; }

    /// <inheritdoc/>
    public string Description { get => "��������� Snap Genshin �������۷۵ġ�"; }

    /// <inheritdoc/>
    public string Author { get => "ϣ��"; }

    /// <inheritdoc/>
    public Version Version { get => new(1, 0, 0, 0); }

    /// <inheritdoc/>
    public void Happen(IContainer container)
    {
        Color pinkColorLight2 = Color.FromArgb(255, 255, 199, 190);
        Color pinkColorLight1 = Color.FromArgb(255, 255, 194, 190);
        Color pinkColor = Color.FromArgb(255, 230, 172, 172);

        // WPFUI
        App.Current.Resources["TextFillColorPrimary"] = pinkColor;
        App.Current.Resources["TextFillColorSecondary"] = pinkColorLight1;
        App.Current.Resources["TextFillColorTertiary"] = pinkColorLight2;

        App.Current.Resources.MergedDictionaries.Add(new()
        {
            Source = new("pack://application:,,,/DGP.Genshin.Skin.Pink;component/Dark.xaml"),
        });
    }
}