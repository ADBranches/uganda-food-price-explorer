"""Filter form for the Uganda Food Price Explorer web application."""

from pathlib import Path

import pandas as pd
from django import forms

from data_loader import load_food_price_csv


class PriceFilterForm(forms.Form):
    """Collect and validate filters used by the analysis results page."""

    commodity = forms.ChoiceField(label="Commodity", required=False)
    market = forms.ChoiceField(label="Market", required=False)
    unit = forms.ChoiceField(label="Measurement unit", required=False)
    start_date = forms.DateField(
        label="Start date",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    end_date = forms.DateField(
        label="End date",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    spike_threshold = forms.FloatField(
        label="Price-spike threshold (%)",
        required=True,
        initial=25.0,
        min_value=0,
        widget=forms.NumberInput(attrs={"min": "0", "step": "0.1"}),
    )

    def __init__(self, *args, dataset_path: str | Path, **kwargs):
        """Populate selectable values from the verified cleaned dataset."""
        super().__init__(*args, **kwargs)
        frame = load_food_price_csv(dataset_path)
        self.fields["commodity"].choices = self._build_choices(frame, "commodity", "All commodities")
        self.fields["market"].choices = self._build_choices(frame, "market", "All markets")
        self.fields["unit"].choices = self._build_choices(frame, "unit", "All units")

    @staticmethod
    def _build_choices(frame: pd.DataFrame, column: str, empty_label: str) -> list[tuple[str, str]]:
        """Return an empty option followed by sorted unique dataset values."""
        values = sorted(str(value) for value in frame[column].dropna().unique())
        return [("", empty_label), *((value, value) for value in values)]

    def clean(self):
        """Reject reversed dates while preserving field-specific validation."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date must be on or before end date.")
        return cleaned_data
